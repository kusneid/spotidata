import os
import clickhouse_connect
from dotenv import load_dotenv
from loguru import logger

def init_clickhouse():
    try:
        client = clickhouse_connect.get_client(
            host='clickhouse',
            port=8123,
            username='default',
            password='default'
        )
        logger.info("Connected to Clickhouse successfully.")
        return client
    except Exception as e:
        logger.error(f"FAILED TO CONNECT TO CLICKHOUSE: {e}")
        return None


def init_env_variables(*keys):
    load_dotenv()
    vars_map = {}
    for key in keys:
        val = os.getenv(key)
        vars_map[key] = val
        logger.info(f"loaded env var {key}={val}")
    return vars_map
