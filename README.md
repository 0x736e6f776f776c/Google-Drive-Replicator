# Google Drive Replicator by TechSnowOwl
A tool to replicate/backup your Google Drive files in a fast and simple matter.
## What does this tool do?
After running the script and authenticating with your Google account, you can copy all the files in a given Google Drive to any other place in Google Drive that you have access to. You have the option to copy the files to multiple destinations at once. You can also select a smart backup option, so that the files you've already copied once will be left out the next time you backup a Drive. This tool works for both Personal/My Drives and Shared Drives.
## Instructions
First of all, go to the [release](https://github.com/techsnowowl/Google-Drive-Replicator/releases/tag/v1.0) and download the *setup.exe*. You could also clone the repository, if you prefer that.

***If you downloaded *setup.exe*:***

1. Run the executable and choose where you wish to save the program files.
2. Open the installed folder, the name should be *Google Drive Replicator*.
3. Now that you're in the folder, you should see two Python (.py) files, a text (.txt) file, a batch (.bat) file, and a JSON (.json) file. Double-click the batch file (*Dependancy Installer.bat*) to install the Python dependencies for the program.
4. After the installer is done, hit any key to close it. The text file and the batch file should now be gone.
5. Double click the *Google_Drive_Replicator.py* file to run the program.
6. Follow the instructions inside the program to make replicas/backups of your Google Drive files.

***If you cloned the repository:***
1. Go to the *Google Drive Replicator* folder.
2. Now that you're in the folder, you should see two Python (.py) files, a text (.txt) file, and a JSON (.json) file. You now need to install the Python dependencies for the    program. There are two ways to do this:  
   Either using a script;
    * Go to my [Python Dependency Installer](https://github.com/techsnowowl/Scripts/tree/main/Python%20Dependency%20Installer) page.  
    * Click one of the download links in the README according to the version you want and save the batch (.bat) file when prompted to do so.  
    * Move the batch script from the folder you downloaded it in to the program's folder.  
    * Double-click the batch file to run it and to install the dependencies.
    * After the installer is done, hit any key to close it.

   Or through the command line;
   * Open the a command line interface (Eg CMD)
   * ```cd``` into the program's folder
   * Run the command ```pip install -r requirements.txt```. The dependencies will now be installed, you can close the command line when it's done.
3. Double click the *Google_Drive_Replicator.py* file to run the program.
4. Follow the instructions inside the program to make replicas/backups of your Google Drive files.

If you experience any issues with the program, please let me know, and I'll try to help you out.
