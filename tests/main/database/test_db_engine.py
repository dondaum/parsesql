import unittest
from parsesql.main.database import db_engine
from parsesql.config.config_reader import Config


class DatabaseEngineTest(unittest.TestCase):

    def setUp(self):
        Config.strategy = "sqllite"

    def test_if_dbengine_class_exists(self):
        """
        test if dbengine class is available
        """
        klass = db_engine.DatabaseEngine()
        self.assertEqual(klass.__class__.__name__, "DatabaseEngine")

    def test_factory_engine_method(self):
        """
        test if factory method returns engine based on param
        """
        engine_options = ["sqllite", "snowflake"]
        # Set snowflake account information
        Config.snowflake_account = Config.data['Snowflake_Account']
        engines = [db_engine.DatabaseEngine(strategy=opt).get_engine()
                   for opt in engine_options
                   ]
        check_engine = all(engine.__class__.__name__ == "Engine"
                           for engine in engines
                           )
        self.assertEqual(check_engine, True)

    def test_if_sqllite_engine_exist(self):
        """
        test if method creates a sqllite engine from sqalchemy
        """
        engine = db_engine.DatabaseEngine().get_engine()
        check_uri = True if "sqlite" in str(engine.url) else False

        self.assertEqual(check_uri, True)

    def test_if_snowflake_engine_exist(self):
        """
        test if method creates a snowflake engine from sqalchemy
        """
        # Set snowflake account information
        Config.snowflake_account = Config.data['Snowflake_Account']
        Config.strategy = 'snowflake'

        engine = db_engine.DatabaseEngine().get_engine()
        check_uri = True if "snowflake" in str(engine.url) else False

        self.assertEqual(check_uri, True)

    def test_if_global_engine_object_exist(self):
        """
        test if the global engine object is not None
        """
        self.assertIsNotNone(db_engine.db_engine)

    def test_if_global_session_object_exist(self):
        """
        test if the global session object is not None
        """
        self.assertIsNotNone(db_engine.Session)


if __name__ == "__main__":
    unittest.main()
