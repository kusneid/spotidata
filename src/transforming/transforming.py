import os
import subprocess
from general.base_utils import init_clickhouse


def run_dbt_transform():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([
        "dbt", "run",
        "--project-dir", current_dir,
        "--profiles-dir", current_dir
    ], check=True)

def run_python_transform():
    client = init_clickhouse()
    client.command("TRUNCATE TABLE tracks")

    insert_query = """
    INSERT INTO tracks (track_name, artist, popularity, lyrics)
    SELECT track_name, artist, popularity, lyrics
    FROM default.tracks
    WHERE track_name NOT LIKE '%(feat%'
      AND length(lyrics) > 0
    """

    client.command(insert_query)

if __name__ == "__main__":
    run_python_transform()
