import unittest
from parsesql.main.database.init_db import create_database
from parsesql.main.database.db_engine import Session
from parsesql.main.database.models import TableDependency
from parsesql import db
import os

DBPATH = os.path.dirname(db.__file__)


class InitDbTest(unittest.TestCase):

    def test_if_build_of_sqlite_db(self):
        """
        test if a sqlite db can be created and located in the db directory
        """
        create_database()
        list_files = os.listdir(DBPATH)
        self.assertIn("parsersql.db", list_files)

    def test_if_session_can_be_established(self):
        """
        test if a session / connection can be build to sqlite db
        """
        create_database()
        error = False
        try:
            session = Session()
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            raise e
            error = True

        self.assertEqual(error, False)

    def test_if_table_exist_in_db(self):
        """
        test if model can be queried and thus if table exist
        """
        create_database()
        error = False
        try:
            session = Session()
            session.query(TableDependency).first()
            session.close()
        except Exception as e:
            print(e)
            raise e
            error = True

        self.assertEqual(error, False)


if __name__ == "__main__":
    unittest.main()
