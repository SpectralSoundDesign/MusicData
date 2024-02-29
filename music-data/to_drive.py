from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = ""

def authenticate_and_upload(file_path, folder_id, file_name):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    drive_service = build('drive', 'v3', credentials=credentials)
    
        # Check if the file already exists in the folder
    existing_files = drive_service.files().list(q=f"'{folder_id}' in parents and name='{file_name}'").execute().get('files', [])

    if existing_files:
        # File already exists, delete it
        file_to_delete = existing_files[0]
        drive_service.files().delete(fileId=file_to_delete['id']).execute()
        print(f'Existing file {file_name} deleted.')
    
    file_metadata = {
        'name' : file_name,
        'parents' : [folder_id]
    }
    
    media = MediaFileUpload(file_path, resumable=True)
    
    file = drive_service.files().create(
        body = file_metadata,
        media_body = media,
        fields = 'id'
    ).execute()
    
    #drive_service.files().delete(fileId=file['id']).execute()
    #print('File removed from the folder.')    
    
    print(f'File ID: {file["id"]}')
    print('File uploaded successfully.')