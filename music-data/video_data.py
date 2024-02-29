from googleapiclient.discovery import build

api_key = ''
youtube = build('youtube', 'v3', developerKey=api_key)

def search_videos(query, max_results=1):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    return response['items']

def get_video_link(video_id):
    return f'https://www.youtube.com/watch?v={video_id}'