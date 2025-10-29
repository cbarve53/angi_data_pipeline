flowchart LR
    A["Public API (JSONPlaceholder)"] --> B["Export App (Python)"]
    B --> C["Minio (raw/date=.../)"]
    C --> D["Loader Script"]
    D --> E["Postgres (raw schema)"]
    E --> F["dbt Staging"]
    F --> G["dbt Intermediate"]
    G --> H["dbt Marts"]
    H --> I["Optional: Curated export to Minio"]