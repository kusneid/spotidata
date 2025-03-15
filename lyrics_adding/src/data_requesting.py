import re

def clean_lyrics(lyrics):
    lyrics = lyrics.replace("'", "''")  
    lyrics = lyrics.replace("\\", "\\\\")  
    lyrics = re.sub(r"[\x00-\x1F\x7F]", "", lyrics)   
    return lyrics

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
        return clean_lyrics(song.lyrics)
    
    print(f"No lyrics found for:{artist_name} - {track_name}")  
    return ""