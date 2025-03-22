from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='spotidata',
    start_date=datetime(2023, 1, 1),
    schedule='@hourly',
    catchup=False
) as dag:

    # 1) Создание/обновление виртуального окружения (один раз при первом запуске)
    create_venv = BashOperator(
        task_id='create_venv',
        bash_command="""
        python -m venv /opt/airflow/my_venv \
        && source /opt/airflow/my_venv/bin/activate \
        && chown -R airflow: /opt/airflow/my_venv \
        && /opt/airflow/my_venv/bin/pip install --no-cache-dir -r /opt/airflow/requirements.txt
        """
    )

    data_ingest = BashOperator(
        task_id='data_ingest',
        bash_command="""
        source /opt/airflow/my_venv/bin/activate \
        && python /opt/airflow/src/data_ingesting/src/data_ingest.py "haha"
        """
    )

    lyrics_enricher = BashOperator(
        task_id='lyrics_enricher',
        bash_command="""
        source /opt/airflow/my_venv/bin/activate \
        && python /opt/airflow/src/lyrics_adding/src/lyrics_enricher.py
        """
    )

    transform = BashOperator(
        task_id='transform',
        bash_command="""
        source /opt/airflow/my_venv/bin/activate \
        && python /opt/airflow/src/transforming/src/transforming.py
        """
    )

    create_venv >> data_ingest >> lyrics_enricher >> transform
