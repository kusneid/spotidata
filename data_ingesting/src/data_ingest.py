import main
import sys
import time
from loguru import logger


def create_tables_with_tracks(client):
    q = """
   CREATE TABLE IF NOT EXISTS default.tracks (
    track_id String,
    track_name String,
    artist String,
    popularity UInt32
) ENGINE = MergeTree()
ORDER BY track_id;

    """
    client.command(q)




def fetch_tracks(spotify_client, query):
    data = []
    offset = 0
    limit = 50
    while offset < 100:
        batch = min(limit, 100 - offset)
        r = spotify_client.search(
            q=query,
            type='track',
            limit=batch,
            offset=offset,
            market='US')
        tracks = r['tracks']['items']
        data.extend(tracks)
        offset += batch
        if len(tracks) < batch:
            break
    return data


def ingest_top_100_tracks(click_client, spotify_client, query_argument):
    create_tables_with_tracks(click_client)
    tracks = fetch_tracks(spotify_client, query=query_argument)
    d = []
    for t in tracks:
        i = t.get('id', '')
        n = t.get('name', '')
        p = t.get('popularity', 0)
        a = t.get('artists', [])
        a_str = ", ".join(x['name'] for x in a)
        d.append([i, n, a_str, p])
    if d:
        click_client.insert(
            'default.tracks',
            d,
            column_names=[
                'track_id',
                'track_name',
                'artist',
                'popularity'])


def run_ingest(args=None):
    query_argument = sys.argv[1]
    create_tables_with_tracks(main.CLICK_CLIENT)
    if not hasattr(
            main,
            'CLICK_CLIENT') or not hasattr(
            main,
            'SPOTIFY_CLIENT'):
        logger.error("Global clients not found.")
        return
    c = main.CLICK_CLIENT
    s = main.SPOTIFY_CLIENT
    t = time.time()
    ingest_top_100_tracks(c, s, query_argument)
    e = time.time() - t
    logger.info(f"Ingest done in {e:.2f}s.")


if __name__ == "__main__":
    main.main()
    run_ingest()
