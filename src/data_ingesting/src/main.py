import general.base_utils as general
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from loguru import logger


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
    envs = general.init_env_variables('SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET')

    CLICK_CLIENT = general.init_clickhouse()
    if CLICK_CLIENT is None:
        logger.error("Clickhouse client initialization failed. Exiting.")
        return

    SPOTIFY_CLIENT = init_spotify(envs['SPOTIFY_CLIENT_ID'], envs['SPOTIFY_CLIENT_SECRET'])
    if SPOTIFY_CLIENT is None:
        logger.error("Spotify client initialization failed. Exiting.")
        return

    logger.info("main.py: Initialization complete.")


if __name__ == "__main__":
    main()
