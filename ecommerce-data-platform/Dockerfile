FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements-dbt.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dbt.txt
COPY . .
ENV PYTHONPATH=/app
CMD ["bash", "scripts/run_pipeline.sh"]
