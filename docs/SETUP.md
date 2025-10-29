# Setup guide — angi_data_pipeline

## Prerequisites
- Docker
- Local Kubernetes of your choice (kind, minikube, k3d)
- kubectl configured to your local cluster
- git
- Python 3.9+
- (Optional) GitLab runner if you want to run CI

This guide assumes `kind` but you can adapt it.

## 1. Start a local cluster (kind example)
```bash
kind create cluster --name angi-demo
kubectl cluster-info --context kind-angi-demo || true
```

## 2. Deploy Minio and PostgreSQL
```bash
kubectl apply -f k8s/minio-namespace.yaml
kubectl apply -f k8s/minio-deployment.yaml
kubectl apply -f k8s/minio-service.yaml

kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

Wait for pods to be `Running`. Use `kubectl get pods -n minio` and `kubectl get pods`.

## 3. Configure local environment for dbt
- Copy `dbt_project/profiles.yml.template` → `~/.dbt/profiles.yml` and edit credentials to match `k8s/postgres` service or port-forward.
- Example port-forward:
```bash
kubectl port-forward svc/postgres 5432:5432
# Now connect to localhost:5432
```

## 4. Run the export app locally (development)
Install requirements:
```bash
python -m venv venv
source venv/bin/activate
pip install -r export_app/requirements.txt
```

Set environment variables (example for Minio):
```bash
export MINIO_ENDPOINT=localhost:9000
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin
export MINIO_SECURE=false
```

Run exporter (it will create `raw/` partitions in Minio):
```bash
python export_app/main.py --limit 100
```

## 5. Load raw data into Postgres
Use the loader script:
```bash
python export_app/loader.py --minio-bucket angi-raw --table raw_events
```

## 6. Run dbt
From `dbt_project/`:
```bash
dbt deps
dbt seed
dbt run
dbt test
dbt docs generate
dbt docs serve
```

## 7. GitLab CI/CD
The `.gitlab-ci.yml` demonstrates stages: build, deploy, transform, test. To run in GitLab, push repository to your GitLab instance and configure runners.

---

If anything in this guide is unclear, check the repo files for examples and templates.
