import json
import os
from pathlib import Path, WindowsPath
from util.logger_service import LoggerMixin


class Configuration(LoggerMixin):
    def __init__(self, filename:str):
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.filename = filename
        self.configfilepath = os.path.join(self.abspath, self.filename)
        self.data = self.read()
        self.sqldir = self.get_sql_directory()
        self.file_extension = self.data['file_extension']
        self.snowflake_account = self.data['Snowflake_Account']

    def read(self):
        try:
            with open(self.configfilepath) as json_data_file:
                return json.load(json_data_file)
        except Exception as e:
            self.logger.info(f"Cannot open file {self.filename}. See this error: {e}")

    def get_sql_directory(self):
        """
        Use Pathlib as it is transforming the path correctly to the given os
        """
        return Path(self.data['sqldirectory'])

Config = Configuration(filename='configuration.json')
