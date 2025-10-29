# Loader: read JSON objects from Minio and insert into Postgres
import os, io, json, argparse
from minio import Minio
import psycopg2
from psycopg2.extras import execute_batch

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() in ("1","true","yes")
BUCKET = os.getenv("MINIO_BUCKET", "angi-raw")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "angi")
PG_USER = os.getenv("PG_USER", "angi")
PG_PASS = os.getenv("PG_PASS", "angi_pass")

client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=MINIO_SECURE)

def list_objects(prefix="raw/"):
    return client.list_objects(BUCKET, prefix=prefix, recursive=True)

def load_into_postgres(table="raw_posts"):
    conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS)
    cur = conn.cursor()
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {table} (
        id int PRIMARY KEY,
        userId int,
        title text,
        body text,
        raw_key text
    );
    ''')
    conn.commit()

    objs = list(list_objects("raw/"))
    rows = []
    for obj in objs:
        data = client.get_object(BUCKET, obj.object_name)
        content = data.read().decode("utf-8")
        payload = json.loads(content)
        rows.append((payload.get("id"), payload.get("userId"), payload.get("title"), payload.get("body"), obj.object_name))
        if len(rows) >= 100:
            execute_batch(cur, f"INSERT INTO {table} (id,userId,title,body,raw_key) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", rows)
            conn.commit()
            rows = []
    if rows:
        execute_batch(cur, f"INSERT INTO {table} (id,userId,title,body,raw_key) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", rows)
        conn.commit()
    cur.close()
    conn.close()
    print("Loaded objects into", table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", default="raw_posts")
    args = parser.parse_args()
    load_into_postgres(table=args.table)
