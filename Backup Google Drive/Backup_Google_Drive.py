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
        # Query user to find out wether we're looking at a Personal/My or Shared Drive as source for the backup
        print('Do you want to backup files from a Personal/My or Shared Drive?')
        source_drive_type = str(input('Enter \'P\' for a Personal/My Drive or \'S\' for a Shared Drive: '))
        source_drive_type = source_drive_type.lower()
        source_drive_type = ClosedQuestionLoop(source_drive_type, 'p', 's')

        # Fetching data for Personal Drive
        if(source_drive_type == 'p'):
            personal_drive_datatype = ''
            personal_drive_datatype = FolderOrDriveLoop(personal_drive_datatype)
            if(personal_drive_datatype == 'f'):
                folder_link = input('Please enter the link to the folder in your Personal/My Drive that you\'d like to backup: ')
                folder_id = ''
                folder_id = GrabId(folder_link, folder_id)
                query = f"parents = '{folder_id}'"
                request = service.files().list(q=query).execute()
            else:
                request = service.files().list().execute()

        # Fetching data for Shared Drive
        else:
            shared_drive_datatype = ''
            shared_drive_datatype = FolderOrDriveLoop(shared_drive_datatype)
            if(shared_drive_datatype == 'f'):
                folder_link = input('Please enter the link of the folder in the selected Shared Drive that you\'d like to backup: ')
                folder_id = ''
                folder_id = GrabId(folder_link, folder_id)
                query = f"parents = '{folder_id}'"
                request = service.files().list(q=query,
                                               supportsAllDrives=True
                                               ).execute()
            else:
                drive_link = str(input('Please enter the link to the *ROOT* of the Shared Drive you\'re trying to backup: '))
                drive_id = 'blyat'
                drive_id = GrabId(drive_link, drive_id)
                request = service.files().list(corpora='drive',
                                               driveId=drive_id,
                                               includeItemsFromAllDrives=True,
                                               supportsAllDrives=True
                                               ).execute()
        files = request.get('files')
        nextPageToken = request.get('nextPageToken')
        while nextPageToken:
            request = service.files().list(q=query, pageToken=nextPageToken).execute()
            files.extend(request.get('files'))
            nextPageToken = request.get('nextPageToken')
        df = pn.DataFrame(files)

        try:
            destinations_amount = int(input('To how many destinations do you wish to backup your files? How many folder and/or Drives? '))
        except ValueError:
            destinations_amount = int(input('Error: please enter an integer/a non-decimal number: '))

        destination_parents_ids = []
        i = 0
        while i != destinations_amount:
            i += 1
            destination_link = input('Please enter the link of destination ' + str(i) + 
                                     ' (If you wish to backup to a Personal/My Drive, create a folder in there and enter the link to it here"): '
                                     )
            destination_id = ''
            if(destination_link.lower()!= 'm'):
                destination_id = GrabId(destination_link, destination_id)
            destination_parents_ids.append(destination_id)

        source_file_ids = []
        for index, rows in df.iterrows():
            if rows.mimeType == 'application/vnd.google-apps.folder':
                continue
            file_id = rows.id
            file_metadata = {'parents': destination_parents_ids}
            service.files().copy(
            fileId=file_id,
            body=file_metadata,
            supportsAllDrives=True
            ).execute()

# Loop until the user's input is valid
def ClosedQuestionLoop(var, value_1, value_2):
    while(True):
        if(var != value_1 and var != value_2):
            var = str(input('Invalid input. Please try again and only enter \'' + value_1 + '\' or \'' + value_2 + '\': '))
            var = var.lower()
        else:
            break
    return var

# Grab the id from a Google Drive link
def GrabId(link, id):
    while(True):
        if('https://' in link):
            id = link.strip(link[:43]) # Removing everything from the link except the drive id
        elif('drive.google.com/drive/u/' in link):
            id = link.strip(link[:35]) # Removing everything from the link except the drive id
        else:
            link = str(input('Invalid link. Please enter a link to the *ROOT* of a Shared Google Drive: '))
            continue
        break
    return id


# Loop until it's known wether the user wants to backup a specific folder or the entire specified Drive
def FolderOrDriveLoop(var):
    print('Do you wish to backup all the files in the Drive or just one specific folder?')
    var = input('Enter \'A\' for all files or \'F\' for a specific folder: ')
    var = var.lower()
    var = ClosedQuestionLoop(var, 'a', 'f')
    return var

if __name__ == '__main__':
    main()