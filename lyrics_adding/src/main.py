from loguru import logger
import os
import autopep8
import clickhouse_connect 
from dotenv import load_dotenv
from lyricsgenius import Genius



def init_env_variables():
    try:
        load_dotenv()
        logger.info("Environment variables loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")
    return os.getenv('GENIUS_ACCESS_TOKEN')

def init_clickhouse():
    try:
        client = clickhouse_connect.get_client(
            host='localhost',
            port=8123,
            username='default',
            password='default'
        )
        logger.info("Connected to Clickhouse successfully.")
        return client
    except Exception as e:
        logger.error(f"FAILED TO CONNECT TO CLICKHOUSE: {e}")
        return None


def init_genius():
    genius_access_token = init_env_variables()
    return Genius(genius_access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

def main():
    global GENIUS_INSTANCE, CLICKHOUSE_INSTANCE
    GENIUS_INSTANCE = init_genius()
    CLICKHOUSE_INSTANCE = init_clickhouse()
    
    
    
    
if __name__ == "__main__":
    main()