# Upwork portfolio copy

**Title:** E-commerce ETL/ELT Data Platform | Python, Airflow, dbt, PostgreSQL

**Project type:** Personal demonstration project using synthetic data.

**Problem:** E-commerce teams need consistent daily revenue and customer metrics, but raw order events include cancellations, returns and varying product categories.

**Solution:** Built an end-to-end, reproducible ETL/ELT demonstration. Python generates and validates synthetic order events; an idempotent PostgreSQL upsert stages raw data; dbt creates tested staging and analytics models; Apache Airflow optionally orchestrates and retries each step. Docker Compose simplifies local deployment, while GitHub Actions tests Python code.

**Deliverables:** Executable code, reproducible sample dataset, SQL transformations, quality checks, Docker setup, orchestration DAG, architecture diagram and README.

**Disclaimer:** Self-directed portfolio project. No actual business/customer data or unverified business impact claims.
