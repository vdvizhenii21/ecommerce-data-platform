#!/usr/bin/env bash
set -euo pipefail
python -m src.generate_data
python -m src.load
python -m src.checks
dbt deps --project-dir dbt --profiles-dir dbt
dbt build --project-dir dbt --profiles-dir dbt
printf '\nPipeline finished successfully.\n'
