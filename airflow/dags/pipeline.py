from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

q = "Weeknd"

with DAG(
    dag_id='spotidata',
    start_date=datetime(2023, 1, 1),
    schedule='@hourly',
    catchup=False
) as dag:

    create_venv = BashOperator(
        task_id='create_venv',
        bash_command="""
        mkdir -p /opt/airflow/venv \
        || chown -R airflow /opt/airflow \
        && python -m venv /opt/airflow/venv \
        && source /opt/airflow/venv/bin/activate \
        && /opt/airflow/venv/bin/pip install pendulum --only-binary pendulum \
        && /opt/airflow/venv/bin/pip install -r /opt/airflow/requirements.txt
        """
    )

    data_ingest = BashOperator(
        task_id='data_ingest',
        bash_command=f"""
        source /opt/airflow/venv/bin/activate \
        && python /opt/airflow/src/data_ingesting/src/data_ingest.py {q}
        """
    )

    lyrics_enricher = BashOperator(
        task_id='lyrics_enricher',
        bash_command="""
        source /opt/airflow/venv/bin/activate \
        && python /opt/airflow/src/lyrics_adding/src/lyrics_enricher.py
        """
    )

    transform = BashOperator(
        task_id='transform',
        bash_command="""
        source /opt/airflow/venv/bin/activate \
        && python /opt/airflow/src/transforming/transforming.py
        """
    )

    create_venv >> data_ingest >> lyrics_enricher >> transform
