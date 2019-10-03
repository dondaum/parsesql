from config.config_reader import Config
import os

class FileFinder(object):
    def __init__(self):
        self.type      =  Config.file_extension
        self.targetdir =  Config.sqldir

    def sayWhatYouSearch(self):
        print(f'Im seachring all files with the extension {self.type}')
        print(f'Im seachring those files in the following target dir {self.targetdir}')

    def get_list_of_folder(self):
        print(self.targetdir)
        return os.listdir(self.targetdir)

    def getListOfFiles(self, dirName=None):
        print('Start looking for files')
        # create a list of file and sub directories 
        # names in the given directory
        if dirName:
            print('There is a direname')
        if self.targetdir:
            ('i chosse the instance variable')
        print(dirName)
        dirName = dirName or self.targetdir
        listOfFile = os.listdir(dirName)
        allFiles = list()
        #print(f"Found: {allFiles}")
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)
        # filter out sql files
        allFiles = [file for file in allFiles if file.endswith(f".{self.type}")]
        return allFiles
