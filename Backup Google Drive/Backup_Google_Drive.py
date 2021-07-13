from Google import Create_Service
import pandas as pn

def main():
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Create the Drive API Service
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,SCOPES)

    # Beginning of the main loop
    while(True):
        # Query user to find out wether we're looking at a Personal or Shared Drive as source for the backup
        print('Do you want to backup files from a Personal or Shared Drive?')
        source_drive_type = str(input('Enter \'P\' for a Personal Drive or \'S\' for a Shared Drive: '))
        source_drive_type = source_drive_type.lower()
        ClosedQuestionLoop(source_drive_type, 'p', 's')

        # Fetching data for Personal Drive
        if(source_drive_type == 'p'):
            print('Do you wish to backup all the files in the specified Drive or just one specific folder?')
            personal_drive_datatype = input('Enter \'A\' for all files or \'F\' for a specific folder: ')
            print('\n')
            personal_drive_datatype = personal_drive_datatype.lower()
            ClosedQuestionLoop(personal_drive_datatype, 'a', 'f')
            if(personal_drive_datatype == 'f'):
                folder_link = input('Please enter the link of the folder in your Personal Drive that you\'d like to backup: ')
                folder_id = ''
                GrabId(folder_link, folder_id)
                query = f"parents = '{folder_id}'"
                request = service.files().list(q=query).execute()
            else:
                request = service.files().list().execute()
        # Fetching data for Shared Drive
        else:
            drive_link = str(input('Please enter the link to the *ROOT* of the Shared Drive you\'re trying to backup: '))
            drive_id = ''
            GrabId(drive_link, drive_id)
            request = service.files().list(corpora='drive', driveId=drive_id, includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
        files = request.get('files')
        nextPageToken = request.get('nextPageToken')
        while nextPageToken:
            request = service.files().list(q=query).execute()
            files.extend(request.get('files'))
            nextPageToken = request.get('nextPageToken')

# Loop until the user's input is valid
def ClosedQuestionLoop(var, value_1, value_2):
    while(True):
        if(var != value_1 and var != value_2):
            var = str(input('Invalid input. Please try again and only enter \'' + value_1 + '\' or \'' + value_2 + '\': '))
            var = var.lower()
        else:
            break

# Grab the id from a Google Drive link
def GrabId(link, id):
    while(True):
        if('https://' in link):
            id = link.strip(link[:43]) # Removing everything from the link except the drive id
            break
        elif('drive.google.com/drive/u/' in link):
            id = link.strip(link[:35]) # Removing everything from the link except the drive id
            break
        else:
            link = str(input('Invalid link. Please enter a link to the *ROOT* of a Shared Google Drive: '))

def FolderOrDriveLoop(var):
    print('Do you wish to backup all the files in the specified Drive or just one specific folder?')
    var = input('Enter \'A\' for all files or \'F\' for a specific folder: ')
    print('\n')
    var = var.lower()
    ClosedQuestionLoop(var, 'a', 'f')
    """
    service.files().copy(
        fileId=source_file_id,
        body=file_metadata
        ).execute()

    """

if __name__ == '__main__':
    main() 