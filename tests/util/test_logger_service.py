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
from tests.helper.config_helper import JsonConfigGenerator
from parsesql.util import logger_service


class LoggerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggerTest.create_config().create()

    @staticmethod
    def create_config(level="INFO"):
        config = JsonConfigGenerator(
            sqldirectory="/A/C/Desktop/views",
            file_extension="sql",
            strategy="sqllite",
            Snowflake_Account={
                "user": "user",
                "password": "password",
                "account": "account",
                "database": "database",
                "schema": "schema",
                "warehouse": "warehouse",
            },
            logging={
                "format": '[%(asctime)s] [%(processName)-10s] [%(name)s] '
                          '[%(levelname)s] -> %(message)s',
                "level": f"{level}",
            }
        )
        return config

    def test_if_logger_class_exist(self):
        """
        test if a logging class with the correct name exist
        """
        klass = logger_service.LoggerMixin()
        self.assertEqual(klass.__class__.__name__, "LoggerMixin")

    def test_base_logging_is_info(self):
        """
        test if the base logging level is level info=20
        """
        log = logger_service.LoggerMixin()
        self.assertEqual(log.logger.getEffectiveLevel(), 20)

    def test_if_logger_logs_messages(self):
        """
        test if the logger mixin logs messages
        """
        error = False
        log = logger_service.LoggerMixin()
        try:
            log.logger.info('This is a test message')
        except AttributeError as e:
            print(e)
            error = True
        self.assertEqual(error, False)


if __name__ == "__main__":
    unittest.main()
