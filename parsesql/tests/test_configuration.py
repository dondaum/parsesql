import unittest
from config import config_reader
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
        klass = config_reader.Configuration(filename='example_configuration.json')
        self.assertEqual(klass.__class__.__name__, "Configuration")

    def test_if_path_object_gets_created(self):
        """
        test if config object is an instance of Path class
        """
        c = config_reader.Configuration(filename='example_configuration.json')
        self.assertIsInstance(c.get_sql_directory(), Path)


if __name__ == "__main__":
    unittest.main()