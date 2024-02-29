from lyricsgenius import Genius
import os

output_folder = 'lyrics'

# Replace 'YOUR_API_KEY' with your actual Genius API key
GENIUS_API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.genius.com'

def get_lyrics(playlist_data):
    # Replace 'YOUR_API_KEY' with the API key you obtained from Genius
    genius = Genius(GENIUS_API_KEY)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for track in playlist_data:
        try:
            # Search for a song by name and artist
            song = genius.search_song(track['Title'], track['Artist'])

            # Write the lyrics to a separate file for each song
            if song:
                output_file_path = os.path.join(output_folder, f"{track['Title']}_{track['Artist']}_lyrics.txt")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(f"Title: {track['Title']}\n")
                    output_file.write(f"Artist: {track['Artist']}\n")
                    output_file.write(f"Lyrics:\n{song.lyrics}\n")
            else:
                print(f"Song not found: {track['Title']} by {track['Artist']}")
        except TimeoutError as e:
            print(f"Timeout error: {e}. Skipping {track['Title']} by {track['Artist']}")
            # Handle the error, e.g., skip the request or retry

