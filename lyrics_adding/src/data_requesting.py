def get_tracklist(clickhouseInstance):
    result = clickhouseInstance.query("SELECT artist, track_name FROM tracks") 
    artistlist = [row[0] for row in result.result_rows]
    tracklist = [row[1] for row in result.result_rows]

    print(f"Fetched tracklist: {tracklist}")
    print(f"Fetched artistlist: {artistlist}")
    return tracklist, artistlist
    
def get_lyrics(track_name, artist_name, geniusInstance):
    print(f"Searching lyrics for:{artist_name} - '{track_name}'") 

    song = geniusInstance.search_song(track_name,artist_name)
    
    if song:
        print(f"Found lyrics for:{artist_name} - {track_name}")  
        return song.lyrics
    
    print(f"No lyrics found for:{artist_name} - {track_name}")  
    return ""