# Simple exporter: fetch sample data from JSONPlaceholder and upload partitioned JSON to Minio
import os
import json
import requests
from minio import Minio
from datetime import datetime
import argparse

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() in ("1","true","yes")

BUCKET = os.getenv("MINIO_BUCKET", "angi-raw")

client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=MINIO_SECURE)

def ensure_bucket():
    if not client.bucket_exists(BUCKET):
        client.make_bucket(BUCKET)
        print("Created bucket", BUCKET)

def fetch_posts(limit=100):
    # sample public API with JSON data (posts)
    r = requests.get("https://jsonplaceholder.typicode.com/posts")
    r.raise_for_status()
    data = r.json()
    return data[:limit]

def upload_partitioned(items):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    prefix = f"raw/date={today}/"
    for i, item in enumerate(items):
        key = f"{prefix}post_{item['id']}.json"
        data = json.dumps(item).encode("utf-8")
        client.put_object(BUCKET, key, data, length=len(data), content_type="application/json")
        if (i+1) % 10 == 0:
            print("Uploaded", i+1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    ensure_bucket()
    items = fetch_posts(limit=args.limit)
    upload_partitioned(items)
    print("Done uploading", len(items))
