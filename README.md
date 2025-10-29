# angi_data_pipeline

An end-to-end demo data engineering pipeline using:
- Kubernetes (local cluster)
- Minio (S3-compatible object storage)
- PostgreSQL (data warehouse)
- dbt (data transformations & docs)
- GitLab CI/CD (pipeline automation)
- Python export application

This repository contains code, manifests, dbt models, CI config, and documentation to run the full pipeline locally.

## Contents
See the repository tree for files and locations. Key items:
- `export_app/` : Python data export app (fetches public API, stores partitioned JSON to Minio)
- `k8s/` : Kubernetes manifests (Minio, Postgres, Deployments, Services)
- `db/` : Database initialization scripts
- `dbt_project/` : dbt project (models, tests, docs)
- `.gitlab-ci.yml` : Example GitLab CI pipeline
- `README.md` : This file

## Quick summary of the pipeline flow
1. export_app fetches data from a public API and writes partitioned JSON files to Minio (raw/)
2. Loader reads raw JSON from Minio and loads into Postgres staging tables
3. dbt runs staging → intermediate → mart models, with tests and docs
4. (Optional) dbt or script exports curated results back to Minio (curated/)

## How to use
Follow detailed setup in `docs/SETUP.md`.

---

For complete instructions, manifests and examples, see `docs/SETUP.md` in this repository.
