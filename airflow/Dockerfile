FROM apache/airflow:latest

USER root
RUN apt-get update && apt-get install -y \
    python3-venv \
    python3-distutils \
 && rm -rf /var/lib/apt/lists/*

 RUN mkdir -p /opt/airflow/venv \
 && chown -R airflow /opt/airflow

USER airflow
WORKDIR /opt/airflow
