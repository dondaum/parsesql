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
from parsesql.config import config_reader
from pathlib import Path


class ConfigurationTest(unittest.TestCase):

    def test_if_missing_config_raise_error(self):
        """
        test if wrong file name will exit programm
        """
        with self.assertRaises(SystemExit):
            config_reader.Configuration(filename='ABS')

    def test_if_config_class_exists(self):
        """
        test if configuration class is available
        """
        klass = config_reader.Configuration(
            filename='configuration.json'
        )
        self.assertEqual(klass.__class__.__name__, "Configuration")

    def test_if_path_object_gets_created(self):
        """
        test if config object is an instance of Path class
        """
        c = config_reader.Configuration(filename='configuration.json')
        self.assertIsInstance(c.get_sql_directory(), Path)


if __name__ == "__main__":
    unittest.main()
