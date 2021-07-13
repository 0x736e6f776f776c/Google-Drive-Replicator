from Google import Create_Service
import pandas as pn

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Create the Drive API Service
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,SCOPES)

# drive_id = '0ABCUP1HlzKy8Uk9PVA'
# query = f"parents = '{drive_id}'"

# Beginning of the main loop
while(True):
    # Query user to find out wether we're looking at a Personal or Shared Drive as source for the backup
    print('Do you want to backup files from a Personal or Shared Drive?')
    source_drive_type = str(input('Enter \'P\' for a Personal Drive or \'S\' for a Shared Drive: '))
    source_drive_type = source_drive_type.lower()
    # Loop until the user's input is valid
    while(True):
        if(source_drive_type != 'p' and source_drive_type != 's'):
            source_drive_type = str(input('Invalid input. Please try again and only enter \'P\' or \'S\': '))
            source_drive_type = source_drive_type.lower()
        else:
            break
    # Fetching data for Personal Drive
    if(source_drive_type == 'p'):
        request = service.files().list().execute()
    # Fetching data for Shared Drive
    else:
        drive_link = str(input('Please enter the link to the *ROOT* of the Shared Drive you\'re trying to backup: '))
        while(True):
            if('https://' in drive_link):
                drive_id = drive_link.strip(drive_link[:43]) # Removing everything from the link except the drive id
                break
            elif('drive.google.com/drive/u/' in drive_link):
                drive_id = drive_link.strip(drive_link[:35]) # Removing everything from the link except the drive id
                break
            else:
                drive_link = str(input('Invalid link. Please enter a link to the *ROOT* of a Shared Google Drive: '))
        request = service.files().list(corpora='drive', driveId=drive_id, includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
    files = request.get('files')
    nextPageToken = request.get('nextPageToken')
    while nextPageToken:
        request = service.files().list(q=query).execute()
        files.extend(request.get('files'))
        nextPageToken = request.get('nextPageToken')

    """
    service.files().copy(
        fileId=source_file_id,
        body=file_metadata
        ).execute()

    """