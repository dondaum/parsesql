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
from tests import sql_file_container
from parsesql.main.sql_parser.snowsqlparser import ParseSql

TEST_SQL_FILE_PATH = os.path.dirname(sql_file_container.__file__)


def write_file(content, name):
    """
    Function that creates a file with custom content
    """
    with open(file=name, mode='w') as f:
        f.write(content)


def remove_file(name):
    """
    Function that removes a file
    """
    try:
        os.remove(name)
    except FileNotFoundError as e:
        print(e)


class SnowSqlparserBaseCleanerTest(unittest.TestCase):

    filename = "check1.sql"
    full_file_name = os.path.join(TEST_SQL_FILE_PATH, filename)

    sql_statement = """
        wITH
        /*
        This is a c like comment
        */
            l AS (
                SELECT 'a' aS userid
                ),
            r AS (
                SELECT 'b' as userid -- The answer is 42
                )
        SELECT *
            FROM l LEFT JOIN r ON l.userid = r.userid
        /* This is a c like comment
        */
        ;
        """

    @classmethod
    def setUpClass(cls):
        write_file(content=cls.sql_statement, name=cls.full_file_name)

    def setUp(self):
        self.sqlcontent = ParseSql(self.__class__.full_file_name)

    @classmethod
    def tearDownClass(cls):
        remove_file(name=cls.full_file_name)

    def reload_raw_sql(self):
        self.sqlcontent.filecontent = self.__class__.sql_statement

    def test_if_file_can_be_read(self):
        """
        test if the init of the class can read the sql file and save
        its content
        """
        self.assertIsNotNone(self.sqlcontent.filecontent)

    def test_if_comments_are_removed(self):
        """
        test if comments -- and /* */ can be removed
        """
        self.reload_raw_sql()

        self.sqlcontent._remove_comments()

        comment_text = [
            "The answer is 42",
            "This is a c like comment"
        ]

        for comment in comment_text:
            self.assertNotIn(comment, self.sqlcontent.filecontent)

    def test_if_uppercase_reserved_expressions(self):
        """
        test if all reserved sql expressions gets uppercased
        """
        self.reload_raw_sql()

        self.sqlcontent._uppercase_sql_expressions()

        lowercase_expressions = [
            "wITH",
            "aS",
            "as",
        ]

        for expr in lowercase_expressions:
            self.assertNotIn(expr, self.sqlcontent.filecontent)

    def test_combination_generator(self):
        """
        test if the generator method returns alls combinations from
        a given string
        """
        expected_combinations = [
            'WITH', 'wITH', 'WiTH', 'wiTH', 'WItH', 'wItH', 'WitH', 
            'witH', 'WITh', 'wITh', 'WiTh', 'wiTh', 'WIth', 'wIth', 
            'With', 'with']
        self.reload_raw_sql()
        gen = self.sqlcontent._get_all_reserved_sql_combinations(s='WITH')
        res = [el for el in gen]
        self.assertListEqual(sorted(expected_combinations),
                             sorted(res)
                             )


if __name__ == "__main__":
    unittest.main()
