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
import os
from tests.helper.config_helper import JsonConfigGenerator
from parsesql import app
from parsesql import exampleSql
from parsesql.main.database.db_engine import Session
from parsesql.main.database.models import TableDependency

SQLFILEPATH = os.path.dirname(exampleSql.__file__)


class RunnerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        RunnerTest.create_config().create()

    @staticmethod
    def create_config(level="INFO"):
        config = JsonConfigGenerator(
            sqldirectory=SQLFILEPATH,
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

    def test_if_runner_class_exists(self):
        """
        test if Runner class is available
        """
        klass = app.Runner()
        self.assertEqual(klass.__class__.__name__, "Runner")

    def test_executer_factor_class_method(self):
        """
        test if either a sequential or multprocessing executer gets
        returned
        """
        sequential = app.Runner()._get_executer()
        multi_proc = app.Runner(parallelism=2)._get_executer()
        self.assertEqual(sequential.__class__.__name__,
                         "SequentialExecuter")
        self.assertEqual(multi_proc.__class__.__name__,
                         "MultiProcessingExecuter")

    def test_search_files(self):
        """
        test if files get searched and return
        """
        expected_files = ['old-join.sql',
                          'third.sql',
                          'select_statement.sql',
                          'cte.sql',
                          'with.sql',
                          'old-view.sql']
        ap = app.Runner()
        ap.search_files()
        foundfiles = [os.path.basename(f) for f in ap.allfiles]
        self.assertEqual(sorted(foundfiles), sorted(expected_files))

    def test_start_sql_parsing(self):
        """
        test if start method works
        """
        ap = app.Runner()
        ap.start_sql_parsing()
        self.assertIsNotNone(ap.dependencies)

    def test_single_insert(self):
        """
        test if single insert works
        """
        dep = [{'filename': 'old-join.sql',
                'name': None,
                'tables': ['CUSTOMERS', 'ORDERS', 'PRODUCT']}]
        ap = app.Runner()
        ap.dependencies = dep
        ap._insertdep()

        query = self.query_result()[0]

        self.assertEqual('old-join.sql', query.filename)

    def test_bulk_insert(self):
        """
        test if bulk insert works
        """
        dep = [{'filename': 'old-join.sql',
                'name': None,
                'tables': ['CUSTOMERS', 'ORDERS', 'PRODUCT']}]
        ap = app.Runner()
        ap.dependencies = dep
        ap._bulkinsertdep()

        query = self.query_result()[0]

        self.assertEqual('old-join.sql', query.filename)

    def test_data_load(self):
        """
        test if data load factory maethod  works
        """
        dep = [{'filename': 'old-join.sql',
                'name': None,
                'tables': ['CUSTOMERS', 'ORDERS', 'PRODUCT']}]
        ap = app.Runner()
        ap.dependencies = dep
        ap._data_load()

        query = self.query_result()[0]

        self.assertEqual('old-join.sql', query.filename)

    def test_start(self):
        """
        test if main start method works
        """
        ap = app.Runner(bulk_load=True)
        ap.start()

        query = self.query_result()
        res = []
        for el in query:
            res.append(el.filename)
        self.assertIn('old-join.sql', res)

    def query_result(self):
        session = Session()
        return session.query(TableDependency).all()


if __name__ == "__main__":
    unittest.main()
