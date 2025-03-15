import main
import data_requesting

def enrich_lyrics():
    clickhouseInstance = main.CLICKHOUSE_INSTANCE
    geniusInstance = main.GENIUS_INSTANCE
    tracklist, artistlist = data_requesting.get_tracklist(clickhouseInstance)
    clickhouseInstance.query("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS lyrics String;")
    tracksLength = len(tracklist)
    tracksAdded = 0
    tracksFailed = 0

    for track, artist in zip(tracklist, artistlist):
        lyrics = data_requesting.get_lyrics(track, artist, geniusInstance)
        print(f"tracks processed: {tracksAdded + tracksFailed}/{tracksLength}")
        if lyrics:
            query = f"ALTER TABLE tracks UPDATE lyrics = '{lyrics}' WHERE track_name = '{track.replace("'", "''")}';"
            clickhouseInstance.command(query)
            tracksAdded += 1
            print(f"Lyrics for '{track}' by '{artist}' added successfully.")
            
        else:
            tracksFailed += 1
            print(f"Lyrics not found for '{track}' by '{artist}'.")
        
    
    print("Lyrics enrichment completed.", f"Tracks added: {tracksAdded}", f"Tracks failed: {tracksFailed}", f"{tracksLength} tracks processed.")

if __name__ == "__main__":
    main.main()
    enrich_lyrics()
