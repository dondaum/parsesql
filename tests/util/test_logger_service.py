import unittest
import json
import os
from parsesql.util import logger_service


class JsonConfigGenerator():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_filepath(self):
        from parsesql import config
        jsonname = 'configuration.json'
        configpath = os.path.dirname(config.__file__)
        return os.path.join(configpath, jsonname)

    def create(self):
        with open(self._get_filepath(), 'w') as json_file:
            json.dump(vars(self), json_file, indent=4)

    def remove(self):
        try:
            os.remove(self._get_filepath())
        except Exception as e:
            print(e)


class Logger(unittest.TestCase):

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
                "format": '[%(asctime)s] [%(processName)-10s] [%(name)s] [%(levelname)s] -> %(message)s',
                "level": "INFO",
            }
        )

    @classmethod
    def setUpClass(cls):
        Logger.config.create()

    @classmethod
    def tearDownClass(cls):
        Logger.config.create()

    def test_if_logger_class_exisit(self):
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

    def test_if_configuration_can_change_level(self):
        """
        test if a given logging level in config file can change level
        """
        pass
