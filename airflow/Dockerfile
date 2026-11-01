FROM apache/airflow:2.10.5-python3.11
USER airflow
COPY requirements.txt requirements-dbt.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt -r /tmp/requirements-dbt.txt
COPY --chown=airflow:root src /app/src
COPY --chown=airflow:root sql /app/sql
COPY --chown=airflow:root dbt /app/dbt
COPY --chown=airflow:root airflow/dags /opt/airflow/dags
