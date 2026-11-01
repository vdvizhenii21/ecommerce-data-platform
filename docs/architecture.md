# Architecture

```mermaid
flowchart TD
  A[Synthetic e-commerce CSV] --> B[Python ingestion and validation]
  B --> C[(PostgreSQL raw.orders)]
  C --> D[dbt staging view]
  D --> E[dbt daily_revenue mart]
  D --> F[dbt customer_metrics mart]
  G[Airflow optional DAG] -. orchestrates .-> A
  G -. orchestrates .-> B
  G -. orchestrates .-> D
  H[GitHub Actions] --> I[pytest unit tests]
```

Raw is loaded with `ON CONFLICT` for rerun safety. dbt filters completed orders and tests unique/non-null keys. Airflow is an optional orchestration mode, not required for a successful local demo.
