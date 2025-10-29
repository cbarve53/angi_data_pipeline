# Dockerfile for angi export app
FROM python:3.10-slim

WORKDIR /app
COPY export_app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY export_app/ /app/
CMD ["python", "main.py", "--limit", "100"]
