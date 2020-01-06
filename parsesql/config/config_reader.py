# MIT License

# Copyright (c) 2019 Sebastian Daum

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import sys
from pathlib import Path


class Configuration():
    def __init__(self, filename: str = 'configuration.json'):
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.filename = filename
        self.configfilepath = os.path.join(self.abspath, self.filename)
        self.data = self.read()
        self.sqldir = self.get_sql_directory()
        self.file_extension = self.data['file_extension']
        self.logger_config = {"Logging": self.data['logging']}
        self.strategy = self.data['strategy']
        if self.strategy == "snowflake":
            self.snowflake_account = self.data['Snowflake_Account']

    def read(self):
        try:
            with open(self.configfilepath) as json_data_file:
                return json.load(json_data_file)
        except FileNotFoundError as e:
            print(f"Cannot find file {self.filename}. "
                  f"Please check if file existing. "
                  f"See this error: {e}")
            sys.exit()

    def get_sql_directory(self):
        """
        Use Pathlib as it is transforming the path correctly to the given os
        """
        return Path(self.data['sqldirectory'])


Config = Configuration()
