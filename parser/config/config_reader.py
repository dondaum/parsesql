import json
import os
from pathlib import Path


class Configuration(object):
    def __init__(self, filename:str):
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.filename = filename
        self.configfilepath = os.path.join(self.abspath, self.filename)
        self.data = self.read()
        self.sqldir = self.get_sql_directory()
        self.file_extension = self.data['file_extension']

    def read(self):
        try:
            with open(self.configfilepath) as json_data_file:
                return json.load(json_data_file)
        except Exception as e:
            print(f"Cannot open file {self.filename}. See this error: {e}")

    def get_sql_directory(self):
        """
        Use Pathlib as it is transforming the path correctly to the given os
        """
        return Path(self.data['sqldirectory'])

Config = Configuration(filename='configuration.json')