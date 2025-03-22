import os
import subprocess

def run_dbt_transform():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([
        "dbt", "run",
        "--project-dir", current_dir,
        "--profiles-dir", current_dir
    ], check=True)

if __name__ == "__main__":
    run_dbt_transform()
