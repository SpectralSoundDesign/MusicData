import music_data
import json

# Boy Jams
PLAYLIST_ID = ''
file_path = 'playlist_data.json'

def save_to_json(playlist_data):
    # Save the list of dictionaries to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(playlist_data, json_file)
        
def load_json():
    # Load data from the JSON file
    with open(file_path, 'r') as json_file:
        playlist_data = json.load(json_file)
    
    return playlist_data