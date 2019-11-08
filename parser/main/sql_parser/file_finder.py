from config.config_reader import Config
from util.logger_service import LoggerMixin
import os

class FileFinder(LoggerMixin):
    def __init__(self):
        self.type      =  Config.file_extension
        self.targetdir =  Config.sqldir

    def getListOfFiles(self, dirName=None):
        #self.logger.info('Start looking for files')
        # create a list of file and sub directories 
        # names in the given directory
        # if dirName:
        #     self.logger.info('There is a direname')
        # if self.targetdir:
        #     self.logger.info('i chosse the instance variable')
        dirName = dirName or self.targetdir
        listOfFile = os.listdir(dirName)
        allFiles = list()

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
        if allFiles:
            self.logger.info(f'Recursive Search found files. Number of files found: {len(allFiles)}')

        return allFiles
