from Google import Create_Service
import pandas as pn
import tkinter as tk
from tkinter import filedialog
import random
import string

def main():
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    smart = False # New backup smart or not, default False
    previous_smart = False # Is there a previous smart backup or not, default False
    trashed = False # Is the source file trashed or not, default False
    starred = False # Is the source file starred or not, default False
    completed = [] # The id's of completed files while backing up (placeholder)
    folder_id = '' # The id of the source folder (placeholder)
    drive_id = '' # The id of the Drive (placeholder)
    destination_id = '' # The id of a destination (placeholder)
    parents = [''] # The desired parents of copied files (placeholder)
    query = '' # Placeholder for the search query used to list files
    shared_drive_datatype = '' # Placeholder for shared Drive datatype
    personal_drive_datatype = '' # Placeholder for My Drive datatype
    previous_smart_content = None # Placeholder
    smart_backup = None # Placeholder
    previous_smart_backup = None # Placeholder
    smart_backup = None # Placeholder

    # Create the Drive API Service
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,SCOPES)

    # Beginning of the main loop
    while(True):
        # Query user to find out whether we're looking at a Personal/My or Shared Drive as source for the backup
        print('Do you want to backup files from a Personal/My Drive or a Shared Drive?')
        source_drive_type = str(input('Enter \'P\' for a Personal/My Drive or \'S\' for a Shared Drive: '))
        source_drive_type = source_drive_type.lower()
        source_drive_type = ClosedQuestionLoop(source_drive_type, 'p', 's')

        # Fetching data for Personal Drive
        if(source_drive_type == 'p'):
            personal_drive_datatype = FolderOrDriveLoop(personal_drive_datatype)
            if(personal_drive_datatype == 'f'):
                folder_link = input('Please enter the link to the folder in your Personal/My Drive that you\'d like to backup: ')
                folder_id = GrabId(folder_link, folder_id)
                query = f"parents = '{folder_id}'"
                request = service.files().list(q=query, orderBy='folder, name').execute()
            else:
                request = service.files().list(orderBy='folder, name').execute()

        # Fetching data for Shared Drive
        else:
            shared_drive_datatype = FolderOrDriveLoop(shared_drive_datatype)
            if(shared_drive_datatype == 'f'):
                folder_link = input('Please enter the link of the folder in the selected Shared Drive that you\'d like to backup: ')
                folder_id = GrabId(folder_link, folder_id)
                query = f"parents = '{folder_id}'"
                request = service.files().list(q=query,
                                               orderBy='folder, name',
                                               supportsAllDrives=True
                                               ).execute()
            else:
                drive_link = str(input('Please enter the link to the *ROOT* of the Shared Drive you\'re trying to backup: '))
                drive_id = GrabId(drive_link, drive_id)
                request = service.files().list(corpora='drive',
                                               driveId=drive_id,
                                               orderBy='folder, name',
                                               includeItemsFromAllDrives=True,
                                               supportsAllDrives=True
                                               ).execute()

        # Get a DataFrame of all files and their metadata
        files = request.get('files')
        nextPageToken = request.get('nextPageToken')
        while nextPageToken:
            request = service.files().list(q=query,
                                           orderBy='folder, name',
                                           pageToken=nextPageToken
                                           ).execute()
            files.extend(request.get('files'))
            nextPageToken = request.get('nextPageToken')
        df = pn.DataFrame(files)

        # Query amount of backup destinations to user
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
            if(destination_link.lower()!= 'm'):
                destination_id = GrabId(destination_link, destination_id)
            destination_parents_ids.append(destination_id)

        # Check with the user whether there's a previous smart backup they want the program to keep in mind
        is_previous_smart_backup = str(input('Is there a pervious smart backup which you\'d like the program to keep in mind? Enter \'Y\'(es) or \'N\'(o): '))
        is_previous_smart_backup = is_previous_smart_backup.lower()
        ClosedQuestionLoop(is_previous_smart_backup, 'y', 'n')
        if(is_previous_smart_backup == 'y'):
            print('Please open the file of the previous smart backup:')
            path_previous_smart = tk.filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')],
                                                                title='Select the previous smart backup file',
                                                                initialdir='/',
                                                                defaultextension='.txt'
                                                                )
            if(path_previous_smart == None): # Try again if the user hasn't selected a file
                tk.messagebox.showerror(title='No file found',
                                        message='Please select a text(\'.txt\') file'
                                        )
                path_previous_smart = tk.filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')],
                                                                    title='Select the previous smart backup file',
                                                                    initialdir='/',
                                                                    defaultextension='.txt'
                                                                    )
            update_previous_smart = str(input('Do you wish to update the previous smart backup with the new backup up? Enter \'Y\'(es) or \'N\'(o): '))
            update_previous_smart = update_previous_smart.lower()
            ClosedQuestionLoop(update_previous_smart, 'y', 'n')
            if(update_previous_smart == 'y'):
                previous_smart_backup = open(path_previous_smart, 'r+') # Open previous smart backup read past backed up files and to append newly backed up files
                smart = True
            else:
                previous_smart_backup = open(path_previous_smart) # Open previous smart backup to only read past backed up
            previous_smart_content = previous_smart_backup.read()
            previous_smart = True
        else: # If there is no previous smart backup to keep in mind, check whether the user wants the current backup to be a smart one backup
            is_smart_backup = str(input('Do you wish for the program to remember the files it has already backed up, so that they are skipped in future backups? Enter \'Y\'(es) or \'N\'(o): '))
            is_smart_backup = is_smart_backup.lower()
            ClosedQuestionLoop(is_smart_backup, 'y', 'n')
            if(is_smart_backup == 'y'):
                print('Please choose where to save the smart backup:')
                path_smart_backup = tk.filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')],
                                                                    title='Choose where to save the smart backup',
                                                                    initialdir='/',
                                                                    defaultextension='.txt'
                                                                    )
                if(path_smart_backup == None): # Try again if the user hasn't selected a file
                    tk.messagebox.showerror(title='No file found',
                                            message='Please save the backup as a text(\'.txt\') file'
                                            )
                    path_smart_backup = tk.filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')],
                                                                        title='Choose where to save the smart backup',
                                                                        initialdir='/',
                                                                        defaultextension='.txt'
                                                                        )
                smart_backup = open(path_smart_backup, 'w') # Open new smart backup file to write the file id's to
                smart = True
        
        # The copying algorithm
        for index, rows in df.iterrows():
            if(rows.id in completed):
                continue
            if(rows.mimeType == 'application/vnd.google-apps.folder'):
                source_folder_id = rows.id
                if(source_folder_id in completed):
                    continue
                source_folder = service.files().get(fileId=source_folder_id,
                                                    fields='name',
                                                    supportsAllDrives=True
                                                    ).execute()
                source_folder_name = source_folder.get('name')
                for destination in destination_parents_ids:
                    parents[0] = destination
                    folder_metadata = {'name': source_folder_name,
                                       'parents': parents,
                                       'mimeType': 'application/vnd.google-apps.folder'
                                       }
                    new_folder = service.files().create(body=folder_metadata,
                                                        supportsAllDrives=True,
                                                        fields='id'
                                                        ).execute()
                    new_folder_id = new_folder.get('id')
                    if(previous_smart == True and smart == True):
                        previous_smart_backup.write(source_folder_id + '\n')
                    elif(smart == True):
                        smart_backup.write(source_folder_id + '\n')
                    completed.append(source_folder_id)
                    for index, rows in df.iterrows():
                        file = service.files().get(fileId=rows.id,
                                                        fields='parents',
                                                        supportsAllDrives=True
                                                        ).execute()
                        file_parents = file.get('parents')
                        if(source_folder_id not in file_parents):
                            continue
                        old_file = service.files().get(fileId=rows.id,
                                                        fields='name, id, starred, trashed',
                                                        supportsAllDrives=True
                                                        ).execute()
                        new_file_name = old_file.get('name')
                        trashed = old_file.get('trashed')
                        starred = old_file.get('starred')
                        if(rows.id in completed):
                            continue
                        if(previous_smart == True):
                            if(rows.id in previous_smart_content):
                                continue
                        if(rows.mimeType == 'application/vnd.google-apps.folder'):
                            folder_parents = [new_folder_id]
                            CopyWithFolders(df, folder_parents, service, previous_smart, smart, rows.id, previous_smart_content, completed, previous_smart_backup, smart_backup, parents, new_file_name)
                            continue
                        file_id = rows.id
                        if(previous_smart == True):
                            if(file_id in previous_smart_content):
                                continue
                        folder_parent_id = [new_folder_id]
                        file_metadata = {'name': new_file_name,
                                         'parents': folder_parent_id,
                                         'starred': starred
                                         }
                        service.files().copy(
                        fileId=file_id,
                        body=file_metadata,
                        supportsAllDrives=True
                        ).execute()
                        completed.append(file_id)
                        if(previous_smart == True and smart == True):
                            previous_smart_backup.write(file_id + '\n')
                        elif(smart == True):
                            smart_backup.write(file_id + '\n')
                        continue
            file_id = rows.id
            if(file_id in completed):
                continue
            if(previous_smart == True):
                if(file_id in previous_smart_content):
                    continue
            for destination in destination_parents_ids:
                parents[0] = destination
                old_file = service.files().get(fileId=rows.id,
                                               fields='name, id, starred, trashed, parents',
                                               supportsAllDrives=True
                                               ).execute()
                old_file_parents = old_file.get('parents')
                if(len(old_file_parents[0]) > 5 and old_file_parents[0] != drive_id and old_file_parents[0] != folder_id):
                    break
                new_file_name = old_file.get('name')
                trashed = old_file.get('trashed')
                starred = old_file.get('starred')
                if(trashed == True):
                    continue
                file_metadata = {'name': new_file_name,
                                 'parents': parents,
                                 'starred': starred,
                                 }
                new_file = service.files().copy(
                                                fileId=file_id,
                                                body=file_metadata,
                                                supportsAllDrives=True
                                                ).execute()
                if(previous_smart == True and smart == True):
                    previous_smart_backup.write(file_id + '\n')
                elif(smart == True):
                    smart_backup.write(file_id + '\n')
                completed.append(file_id)
        if(previous_smart == True):
            previous_smart_backup.close()
        if(smart == True and previous_smart != True):
            smart_backup.close()
        completed = []
        print("\nBackup completed!\n")


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
        if('https://' in link and 'drive.google.com/drive/u/' in link):
            id = link[43:] # Grabbing the id from the link
        elif('https://' in link and '/u/' not in link and 'drive.google.com/drive/' in link):
            id = link[39:] # Grabbing id from the link with https:// and with only one user logged in
        elif('drive.google.com/drive/u/' in link):
            id = link[35:] # Grabbing the id from the link if it's been copied without https://
        elif('drive.google.com/drive/' in link):
            id = link[31:] # Grabbing id from the link without https:// and with only one user logged in
        else:
            link = str(input('Invalid link. Please enter a link to the *ROOT* of a Shared Google Drive: '))
            continue
        break
    return id


# Loop until it's known whether the user wants to backup a specific folder or the entire specified Drive
def FolderOrDriveLoop(var):
    print('Do you wish to backup all the files in the Drive or just one specific folder?')
    var = input('Enter \'A\' for all files or \'F\' for a specific folder: ')
    var = var.lower()
    var = ClosedQuestionLoop(var, 'a', 'f')
    return var

def CopyWithFolders(df, destinations, service, previous_smart, smart, source_folder_id, previous_smart_content, completed, previous_smart_backup, smart_backup, parents, source_folder_name):
    for destination in destinations:
        parents[0] = destination
        folder_metadata = {'name': source_folder_name,
                            'parents': parents,
                            'mimeType': 'application/vnd.google-apps.folder'
                            }
        new_folder = service.files().create(body=folder_metadata,
                                            supportsAllDrives=True,
                                            fields='id'
                                            ).execute()
        new_folder_id = new_folder.get('id')
        if(previous_smart == True and smart == True):
            previous_smart_backup.write(source_folder_id + '\n')
        elif(smart == True):
            smart_backup.write(source_folder_id + '\n')
        completed.append(source_folder_id)
        for index, rows in df.iterrows():
            file = service.files().get(fileId=rows.id,
                                            fields='parents',
                                            supportsAllDrives=True
                                            ).execute()
            file_parents = file.get('parents')
            if(source_folder_id not in file_parents):
                continue
            old_file = service.files().get(fileId=rows.id,
                                            fields='name, id, starred, trashed',
                                            supportsAllDrives=True
                                            ).execute()
            new_file_name = old_file.get('name')
            trashed = old_file.get('trashed')
            starred = old_file.get('starred')
            if(rows.id in completed):
                continue
            if(previous_smart == True):
                if(rows.id in previous_smart_content):
                    continue
            if(rows.mimeType == 'application/vnd.google-apps.folder'):
                folder_parents = [new_folder_id]
                CopyWithFolders(df, folder_parents, service, previous_smart, smart, rows.id, previous_smart_content, completed, previous_smart_backup, smart_backup, parents, new_file_name)
                completed.append(rows.id)
                continue
            file_id = rows.id
            folder_parent_id = [new_folder_id]
            file_metadata = {'name': new_file_name,
                                'parents': folder_parent_id,
                                'starred': starred
                                }
            service.files().copy(
            fileId=file_id,
            body=file_metadata,
            supportsAllDrives=True
            ).execute()
            completed.append(file_id)
            if(previous_smart == True and smart == True):
                previous_smart_backup.write(file_id + '\n')
            elif(smart == True):
                smart_backup.write(file_id + '\n')

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    main()
