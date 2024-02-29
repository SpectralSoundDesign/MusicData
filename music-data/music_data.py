import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import certifi
import requests
import video_data
import time

playlist_track_titles = []
playlist_track_artists = []
playlist_track_date = []
playlist_album_titles = []
playlist_track_duration = []
playlist_track_tempo = []
playlist_track_key = []
playlist_track_mode = []
playlist_track_timesig = []
playlist_track_valence = []
playlist_track_energy = []
playlist_track_instrumentalness = []
playlist_track_danceability = []
playlist_track_acousticness = []
playlist_track_loudness = []
playlist_track_popularity = []
playlist_track_video_link = []

keys = {0 : 'C',
        1 : 'C#/Db',
        2 : 'D',
        3 : 'D#/Eb',
        4 : 'E',
        5 : 'F',
        6 : 'F#/Gb',
        7 : 'G',
        8 : 'G#/Ab',
        9 : 'A',
        10 : 'A#/Bb',
        11 : 'B' }

modes = {0 : 'Minor',
         1 : 'Major' }

timesig = {1 : '1/4',
           3 : '3/4',
           4 : '4/4',
           5 : '5/4',
           7 : '7/4'}

CLIENT_ID = ''
CLIENT_SECRET = ''

# Specify the path to the certificate bundle
cert_path = certifi.where()

# Configure requests to use the specified certificate bundle
requests_session = requests.Session()
requests_session.verify = cert_path

# Set up the Spotify API client with the configured requests session
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, requests_session=requests_session))

def create_dict():
    # Define keys for the dictionary
    keys = ['Title', 'Artist', 'Date', 'Album', 'Duration', 'Tempo', 'Time Signature', 'Key', 'Mode', 'Instrumentalness', 'Loudness', 'Valence', 'Energy', 'Danceability', 'Acousticness', 'Popularity', 'Video Link']

    # Zip the arrays together and create a list of dictionaries
    playlist_data = [
        dict(zip(keys, values))
        for values in zip(
            playlist_track_titles,
            playlist_track_artists,
            playlist_track_date,
            playlist_album_titles,
            playlist_track_duration,
            playlist_track_tempo,
            playlist_track_timesig,
            playlist_track_key,
            playlist_track_mode,
            playlist_track_instrumentalness,
            playlist_track_loudness,
            playlist_track_valence,
            playlist_track_energy,
            playlist_track_danceability,
            playlist_track_acousticness,
            playlist_track_popularity,
            playlist_track_video_link
        )
    ]

    return playlist_data

def get_playlist_tracks(playlist_id):
    try:
        time.sleep(5)
        playlist = sp.playlist(playlist_id)
        
        playlist_name = playlist['name']
        tracks = playlist['tracks']['items']
        
        print(f"Playlist Name: {playlist_name}")
        #print("Tracks:")
        
        for index, track in enumerate(tracks, start=1):
            track_id = track['track']['id']
            
            track_name = track['track']['name']
            playlist_track_titles.append(track_name)
            
            artists = ", ".join(artist['name'] for artist in track['track']['artists'])
            playlist_track_artists.append(artists)
            
            release_date = get_release_date(track_id)
            playlist_track_date.append(release_date)
            
            album_title = track['track']['album']['name']
            playlist_album_titles.append(album_title)
            
            track_duration_ms = track['track']['duration_ms']
            track_duration_min = track_duration_ms // (1000 * 60)
            track_duration_sec = (track_duration_ms % (1000 * 60)) // 1000
            formatted_duration = f"{track_duration_min}:{track_duration_sec:02}"
            playlist_track_duration.append(formatted_duration)
            
            audio_features = sp.audio_features(track_id)
            track_tempo = audio_features[0]['tempo']
            playlist_track_tempo.append(track_tempo)
            
            audio_features = sp.audio_features(track_id)
            track_timesig = audio_features[0]['time_signature']
            track_timesig_name = timesig[track_timesig]
            playlist_track_timesig.append(track_timesig_name)
            
            audio_features = sp.audio_features(track_id)
            track_key = audio_features[0]['key']
            track_key_letter = keys[track_key]
            playlist_track_key.append(track_key_letter)
            
            audio_features = sp.audio_features(track_id)
            track_mode = audio_features[0]['mode']
            track_mode_name = modes[track_mode]
            playlist_track_mode.append(track_mode_name)
            
            audio_features = sp.audio_features(track_id)
            track_instrumentalness = audio_features[0]['instrumentalness']
            playlist_track_instrumentalness.append(track_instrumentalness)
            
            audio_features = sp.audio_features(track_id)
            track_loudness = audio_features[0]['loudness']
            track_loudness_tag = str(track_loudness) + ' dB'
            playlist_track_loudness.append(track_loudness_tag)
            
            audio_features = sp.audio_features(track_id)
            track_valence = audio_features[0]['valence']
            playlist_track_valence.append(track_valence)
            
            audio_features = sp.audio_features(track_id)
            track_energy = audio_features[0]['energy']
            playlist_track_energy.append(track_energy)
            
            audio_features = sp.audio_features(track_id)
            track_danceability = audio_features[0]['danceability']
            playlist_track_danceability.append(track_danceability)
            
            audio_features = sp.audio_features(track_id)
            track_acousticness = audio_features[0]['acousticness']
            playlist_track_acousticness.append(track_acousticness)
            
            track_popularity = track['track']['popularity']
            playlist_track_popularity.append(track_popularity)
            
            # get video related info
            artist_and_track = artists + track['track']['name']
            video_results = video_data.search_videos(artist_and_track)

            for result in video_results:
                # title = result['snippet']['title']
                video_id = result['id']['videoId']
                link = video_data.get_video_link(video_id)
                playlist_track_video_link.append(link)
                break
                #print(f"Title: {title}, Video ID: {video_id}, Link: {link}")
            
            #print(f"{index}. {track_name} by {artists}")
            
        return create_dict()
    
    except Exception as e:
        print(f"Error: {e}")

def get_release_date(track_id):
    try:
        track = sp.track(track_id)
        
        release_date = track['album']['release_date']
        
        return release_date
    
    except Exception as e:
        print(f"Error getting release date: {e}")

def get_top_tracks(artist_name):
    results = sp.search(q=artist_name, type='artist')
    
    if results['artists']['items']:
        artist_id = results['artists']['items'][0]['id']
        top_tracks = sp.artist_top_tracks(artist_id)
        
        for track in top_tracks['tracks']:
            print(track['name'])
           
def get_track_id(track_title):
    try:
        results = sp.search(q=track_title, type='track', limit=1)
        
        track_id = results['tracks']['items'][0]['id']
        
        return track_id
        
    except Exception as e:
        print(f"Error: {e}")

