import os
import clickhouse_connect
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from loguru import logger


def init_env_variables():
    try:
        load_dotenv()
        logger.info("Environment variables loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")
    return os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')


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


def init_spotify(client_id, client_secret):
    try:
        spotify_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )
        logger.info("Spotify client initialized successfully.")
        return spotify_client
    except Exception as e:
        logger.error(f"FAILED TO INITIALIZE SPOTIFY CLIENT: {e}")
        return None


def main():
    global CLICK_CLIENT, SPOTIFY_CLIENT

    client_id, client_secret = init_env_variables()

    CLICK_CLIENT = init_clickhouse()
    if CLICK_CLIENT is None:
        logger.error("Clickhouse client initialization failed. Exiting.")
        return

    SPOTIFY_CLIENT = init_spotify(client_id, client_secret)
    if SPOTIFY_CLIENT is None:
        logger.error("Spotify client initialization failed. Exiting.")
        return

    logger.info("main.py: Initialization complete.")


if __name__ == "__main__":
    main()
