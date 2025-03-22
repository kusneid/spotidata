FROM apache/airflow:3.0.0b4-python3.11

USER root
RUN apt-get update && apt-get install -y python3-distutils && rm -rf /var/lib/apt/lists/*
USER airflow
WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
