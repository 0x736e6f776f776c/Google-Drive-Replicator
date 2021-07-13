from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,SCOPES)

folder_id = ['1rCPxx8d6w0OV787OYD11d1lXUq2mL-Uz']
query = f"parents = '{folder_id}'"

request = service.files().list(q=query).execute()
folders = request.get('folders')
nextPageToken = request.get('nextPageToken')
while nextPageToken:
    request = service.files().list(q=query).execute()
    folders.extend(request.get('folders'))
    nextPageToken = request.get('nextPageToken')

"""
for folder in request.get(folders):

"""
file_metadata = original_file_metadata

service.files().copy(
    fileId=source_file_id,
    body=file_metadata
    ).execute()