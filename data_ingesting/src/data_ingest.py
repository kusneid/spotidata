import main
import sys
import time
from loguru import logger


def create_tables_with_tracks(client):
    q = """
   CREATE TABLE IF NOT EXISTS default.tracks (
    track_id String PRIMARY KEY,
    track_name String,
    artist String,
    popularity UInt32
    ) ENGINE = ReplacingMergeTree()
    
    ORDER BY track_id;
    """
    client.command(q)

def delete_duplicates(client):
    q="""OPTIMIZE TABLE tracks FINAL;
    """
    client.command(q)



def fetch_tracks(spotify_client,query):
    years = [
        "2025", "2024", "2023", "2022", "2021",
        "2020", "2019", "2018", "2017", "2016",
        "2015", "2014", "2013", "2012", "2011", "2010"
    ]
    all_tracks = []
    for y in years:
        offset = 0
        limit = 50
        while offset < 100:
            batch = min(limit, 100 - offset)
            resp = spotify_client.search(
                q=f"year:{y}" + ' track:'+query,
                type="track",
                limit=batch,
                offset=offset,
                market="US"
            )
            items = resp["tracks"]["items"]
            all_tracks.extend(items)
            offset += batch
            if len(items) < batch:
                break
    return all_tracks

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
    if args is None:
        args = sys.argv
    if len(args) < 2:
        logger.error("Please provide a query argument.")
        return
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
    delete_duplicates(c)
    e = time.time() - t
    logger.info(f"Ingest done in {e:.3f}s.")


if __name__ == "__main__":
    main.main()
    run_ingest()
