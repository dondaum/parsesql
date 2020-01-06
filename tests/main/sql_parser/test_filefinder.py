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


import unittest
from parsesql.main.sql_parser import file_finder
from parsesql.config.config_reader import Config
from parsesql import exampleSql
from pathlib import Path
import os

SQLFILEPATH = os.path.dirname(exampleSql.__file__)


class FileFinderTest(unittest.TestCase):

    def test_if_filefinder_class_exists(self):
        """
        test if FileFinder class is available
        """
        klass = file_finder.FileFinder()
        self.assertEqual(klass.__class__.__name__, "FileFinder")

    def test_if_files_get_searched(self):
        """
        test if recursive file search method returns the correct list
        of files
        """
        # Change sql directory path in Config class
        Config.sqldir = Path(SQLFILEPATH)

        targetfiles_gen = os.walk(SQLFILEPATH)
        targetfiles = []
        for path, directories, files in targetfiles_gen:
            for file in files:
                if file.endswith(".sql"):
                    targetfiles.append(os.path.join(path, file))

        finder = file_finder.FileFinder()
        foundfiles = finder.getListOfFiles()

        self.assertEqual(sorted(targetfiles), sorted(foundfiles))


if __name__ == "__main__":
    unittest.main()
