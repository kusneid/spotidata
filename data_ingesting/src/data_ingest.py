import os
import clickhouse_connect
from dotenv import load_dotenv
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials


client = clickhouse_connect.get_client( # Connect to Clickhouse
    host='clickhouse',
    port=8123,
    username='default',
    password=''
)

load_dotenv() # Load environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def init_spotify():     # Initialize Spotify client
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

def main():
    init_spotify()

if __name__ == "__main__":
    main()