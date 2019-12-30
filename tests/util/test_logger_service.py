import unittest
import json
import os
from parsesql.util import logger_service
from parsesql import config

CONFIGPATH = os.path.dirname(config.__file__)


class JsonConfigGenerator():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_filepath(self):
        jsonname = 'configuration.json'
        return os.path.join(CONFIGPATH, jsonname)

    def create(self):
        with open(self._get_filepath(), 'w') as json_file:
            json.dump(vars(self), json_file, indent=4)

    def remove(self):
        try:
            os.remove(self._get_filepath())
        except Exception as e:
            print(e)


class LoggerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggerTest.create_config().create()

    @staticmethod
    def create_config(level="INFO"):
        config = JsonConfigGenerator(
            sqldirectory="/Users/sebastiandaum/Desktop/views",
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
