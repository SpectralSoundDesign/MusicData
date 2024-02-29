import music_data
import track_data_to_excel
import to_drive
import lyrics_data
import save_load_json
import os

# Boy Jams
PLAYLIST_ID = ''
DRIVE_FOLDER_ID = ''
DRIVE_LYRICS_FOLDER_ID = ''
# PLAYLIST_ID = ''

def main():
    # load playlist_data json to use
    playlist_data = music_data.get_playlist_tracks(PLAYLIST_ID)
    playlist_data_saved = save_load_json.load_json()
    
    if playlist_data == playlist_data_saved:
        print("Playlist has not been updated. Aborting...")
    else:
        save_load_json.save_to_json(playlist_data)
        save_directory = 'ExcelSheets'#r'/mnt/c/Users/willh/Desktop'
        excel_file_name = 'band-song-info.xlsx'
        lyrics_folder_directory = 'lyrics'
        full_path = f"{save_directory}/{excel_file_name}"
        
        for track in playlist_data:
            print(track)
        
        # create excel of playlist_data
        track_data_to_excel.createExcel(playlist_data, save_directory, excel_file_name)
        
        # get lyrics for tracks in playlist_data
        # lyrics_data.get_lyrics(playlist_data)
        
        # add all files from lyrics folder to lyrics drive folder
        '''for filename in os.listdir(lyrics_folder_directory):
            file_path = os.path.join(lyrics_folder_directory, filename)
            if os.path.isfile(file_path):
                # print(f"File: {filename}")
                full_lyrics_path = f"{lyrics_folder_directory}/{filename}"
                to_drive.authenticate_and_upload(full_lyrics_path, DRIVE_LYRICS_FOLDER_ID, filename)
            elif os.path.isdir(file_path):
                print(f"Folder: {filename}")'''
        
        # add playlist_data excel sheet to drive
        to_drive.authenticate_and_upload(full_path, DRIVE_FOLDER_ID, excel_file_name)

# This block checks if the script is being run as the main program
if __name__ == "__main__":
    main()