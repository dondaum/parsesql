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
import re
from tests import sql_file_container
from parsesql.main.sql_parser.snowsqlparser import (ParseSql,
                                                    LigthSqlTextCleaner,
                                                    BaseSqlTextCleaner,
                                                    TableSqlTextCleaner)
from parsesql.main.sql_parser.sqlExpressions import (RESERVED_SQL_EXPRESSIONS,
                                                     END_STATEMENT)

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
        CREATE OR REPLACE VIEW abs (USER_ID_HEADER) AS
        wITH
        /*
        This is a c like comment
        */
            l AS (
                SELECT 'a' aS userid
                ),
            r AS (
                seLect 'b' as userid -- The answer is 42
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
        self.sql_parser_obj = ParseSql(self.__class__.full_file_name)

    @classmethod
    def tearDownClass(cls):
        remove_file(name=cls.full_file_name)

    def reload_raw_sql(self, string=None):
        if string:
            self.sql_parser_obj.filecontent = string
        else:
            self.sql_parser_obj.filecontent = self.__class__.sql_statement

    def test_if_file_can_be_read(self):
        """
        test if the init of the class can read the sql file and save
        its content
        """
        self.assertIsNotNone(self.sql_parser_obj.filecontent)

    def test_if_comments_are_removed(self):
        """
        test if comments -- and /* */ can be removed
        """
        self.reload_raw_sql()

        self.sql_parser_obj._remove_comments()

        comment_text = [
            "The answer is 42",
            "This is a c like comment"
        ]

        for comment in comment_text:
            self.assertNotIn(comment, self.sql_parser_obj.filecontent)

    def test_if_uppercase_reserved_expressions(self):
        """
        test if all reserved sql expressions gets uppercased
        """
        self.reload_raw_sql()

        self.sql_parser_obj._uppercase_sql_expressions()

        lowercase_expressions = [
            "wITH",
            "aS",
            "as",
            "seLect",
        ]

        for expr in lowercase_expressions:
            self.assertNotIn(expr, self.sql_parser_obj.filecontent)

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
        gen = self.sql_parser_obj._get_all_reserved_sql_combinations(s='WITH')
        res = [el for el in gen]
        self.assertListEqual(sorted(expected_combinations),
                             sorted(res)
                             )

    def test_if_all_sql_combination_consumable(self):
        """
        test if a generator returns all sql reserved keywords
        """
        gen = self.sql_parser_obj._consume_reserved_sql_combinations()
        self.assertIsNotNone(next(gen))

    def test_text_indentation_change(self):
        """
        test if sql text is formated withouht left and right text space
        """
        unformatted = """
          SELECT *
        FROM
         Dual
        """
        str0 = ""
        str1 = "SELECT *"
        str2 = "FROM"
        str3 = "Dual"
        str4 = ""
        exected = '\n'.join([str0, str1, str2, str3, str4])
        self.reload_raw_sql(string=unformatted)
        unindent = self.sql_parser_obj._unintend()
        self.assertEqual(unindent.filecontent, exected)

    def test_remove_header_defintion(self):
        """
        test if sql view header declaration can be removed
        e.g. (col1, col2, col3) AS...
        """
        self.reload_raw_sql()
        self.sql_parser_obj._remove_header_view_col_definition()
        parants = [")", "("]

        check = False
        for paran in parants:
            if paran in self.sql_parser_obj.filecontent.split('\n')[1]:
                check = True

        self.assertEqual(check, False)

    def test_remove_empty_lines(self):
        """
        Test if empty lines can be removed from string
        """
        self.reload_raw_sql()
        self.sql_parser_obj._remove_empty_lines()

        count_empty_lines = 0
        empty_lines = []

        splitted_content = self.sql_parser_obj.filecontent.splitlines()
        for idx, line in enumerate(splitted_content):
            if (line.isspace() or len(line) <= 0):
                empty_lines.append(idx)
                count_empty_lines += 1

        self.assertEqual(count_empty_lines, 0,
                         f"empty line numbers: {empty_lines}")

    def test_base_cleanup(self):
        """
        test if string is correctly left stripped
        """
        clean_list = [
            "CREATE OR REPLACE VIEW abs  AS",
            "WITH",
            "l AS (",
            "SELECT 'a' AS userid",
            "),",
            "r AS (",
            "SELECT 'b' AS userid                 )",
            "SELECT *",
            "FROM l LEFT JOIN r ON l.userid = r.userid",
            ";", ]
        clean_str = "\n".join(clean_list)
        self.reload_raw_sql()
        self.sql_parser_obj._base_clean_up()

        self.assertEqual(self.sql_parser_obj.filecontent, clean_str)


class SnowSqlParserTest(unittest.TestCase):

    filename = "check2.sql"
    full_file_name = os.path.join(TEST_SQL_FILE_PATH, filename)

    sql_statement = """
            CREATE VIEW SAMP.V1 (COL_SUM, COL_DIFF) AS
            with album_info_1976 as
            (
            select m.album_ID, m.album_name, b.band_name
            from music_albums as m inner join music_bands as b
            where m.band_id = b.band_id and album_year = 1976
            ) --This is a comment
            , old_join AS (
            SELECT ID,
            NAME,
            AGE,
            AMOUNT
            FROM CUSTOMERS, /* Old join */
            ORDERS,
            PRODUCT
            WHERE CUSTOMERS.ID = ORDERS.CUSTOMER_ID
            )
            SELECT
            *
            FROM old_join e
            INNER JOIN album_info_1976 a
            ON e.NAME = a.NAME
            ;
        """

    @classmethod
    def setUpClass(cls):
        write_file(content=cls.sql_statement, name=cls.full_file_name)

    def setUp(self):
        self.sql_parser_obj = ParseSql(self.__class__.full_file_name)

    @classmethod
    def tearDownClass(cls):
        remove_file(name=cls.full_file_name)

    def reload_raw_sql(self, string=None):
        if string:
            self.sql_parser_obj.filecontent = string
        else:
            self.sql_parser_obj.filecontent = self.__class__.sql_statement

    def test_keyword_positions(self):
        """
        test if keywords position can be detected correctly
        """
        counter = 0
        for n in RESERVED_SQL_EXPRESSIONS:
            for m in re.finditer(r"\b" + n + r"\b",
                                 self.sql_parser_obj.filecontent):
                counter += 1
        for n in END_STATEMENT:
            if n in self.sql_parser_obj.filecontent:
                cnt = self.sql_parser_obj.filecontent.count(n)
                counter += cnt

        self.assertEqual(len(self.sql_parser_obj.allkeywordPos),
                         counter)

    def test_key_word_pairs(self):
        """
        test if keyword list can be calulated from string
        This test is identical to the actual method. This is bad but
        could not be solved in time
        """
        keywords = self.sql_parser_obj._parse_position_pair()

        parsePair = []
        keywordlist = ['FROM', 'JOIN']
        for searchkey in keywordlist:
            for pos in self.sql_parser_obj._parse_statement(stat=searchkey):
                for allpos in self.sql_parser_obj.allkeywordPos:
                    if pos['endpos'] < allpos:
                        parsePair.append([pos['endpos'], allpos])
                        break

        self.assertEqual(keywords, parsePair)

    def test_parse_statement(self):
        """
        test if search statements can be found with related positions
        """
        keyword = "FROM"
        cont = self.sql_parser_obj.filecontent
        target_list = []
        for m in re.finditer(r"\b" + keyword + r"\b", cont):
            pos = {}
            pos['keyword'] = keyword
            pos['startpos'] = m.start()
            pos['endpos'] = m.end()
            target_list.append(pos)

        self.assertEqual(target_list,
                         self.sql_parser_obj._parse_statement(stat=keyword))

    def test_parse_uncleaned_text(self):
        """
        test if raw text extraction after JOIN and FROM works
        """
        expected = ['music_albums',
                    'CUSTOMERS',
                    'ORDERS',
                    'PRODUCT',
                    'old_join',
                    'music_bands',
                    'album_info_1976']

        target_text = self.sql_parser_obj._parse_uncleaned_text()
        target_str = ''.join(target_text)
        check = True
        for objekt in expected:
            if objekt in target_str:
                check = True
            else:
                check = False

        self.assertEqual(check, True)

    def test_parseFromEnd(self):
        """
        test if dependent table object are parsed
        """
        dependent_objects = ['MUSIC_ALBUMS',
                             'CUSTOMERS',
                             'ORDERS',
                             'PRODUCT',
                             'MUSIC_BANDS',
                             'OLD_JOIN',
                             'ALBUM_INFO_1976']
        parsed_objects = self.sql_parser_obj._parseFromEnd()
        self.assertEqual(sorted(dependent_objects), sorted(parsed_objects))

    def test_oldjoin_detection(self):
        """
        test if old join with WHERE condition can be detected
        """
        old_join = "CUSTOMERS,ORDERS, PRODUCT"
        expected = ["CUSTOMERS", "ORDERS", "PRODUCT"]
        clean = self.sql_parser_obj._detect_old_join(raw=old_join)
        self.assertEqual(sorted(expected), sorted(clean))

    def test_if_comma_are_removed(self):
        """
        test if commas are removed correctly
        """
        uncleaned = "CUSTOMERS, ORDERS, PRODUCT"
        expected = "CUSTOMERS ORDERS PRODUCT"
        clean = self.sql_parser_obj.rm_comma(raw=uncleaned)
        self.assertEqual(expected, clean)

    def test_if_all_after_whitespaced_removed(self):
        """
        test if all after a whitespace can be removed
        """
        uncleaned = ["CUSTOMERS asdassd cass",
                     "ORDERS ioadas"]
        expected = ["CUSTOMERS", "ORDERS"]

        clean = self.sql_parser_obj._rm_after_whitespace(raw=uncleaned)
        self.assertEqual(expected, clean)

    def test_with_name_parsing(self):
        """
        test if the first cte name declared by with can be parsed
        """
        expected = "album_info_1976"
        with_name = self.sql_parser_obj._get_with_name()
        self.assertEqual(expected, with_name)

    def test_cte_name_parsing(self):
        """
        test if cte names can be parsed
        """
        all_ctes = []
        expected = "album_info_1976"

        all_ctes.append(expected)
        parse_ctes = self.sql_parser_obj.get_all_cte_names()
        self.assertEqual(all_ctes, parse_ctes)


class LigthSqlTextCleanerTest(unittest.TestCase):

    test_sql_text = "  CREATE OR REPLACE VIEW abs  AS "

    def test_if_right_whitespace_is_removed(self):
        """
        test whitespace remove right site
        """
        expected_txt = "  CREATE OR REPLACE VIEW abs  AS"
        cleaner = LigthSqlTextCleaner(text=self.__class__.test_sql_text)
        cleaner.removeRightWhiteSpace()
        self.assertEqual(cleaner.text, expected_txt)

    def test_main_start_method(self):
        """
        test if main orchestrator start method works as expected
        """
        expected_txt = "CREATE OR REPLACE VIEW abs  AS"
        cleaner = LigthSqlTextCleaner(text=self.__class__.test_sql_text)
        cleaner.start()
        self.assertEqual(cleaner.text, expected_txt)


class BaseSqlTextCleanerTest(unittest.TestCase):

    test_sql_text = "  CREATE OR REPLACE VIEW abs  AS "

    test_str_list = [' music_albums ',
                     ' CUSTOMERS,\nORDERS,\nPRODUCT\n',
                     ' old_join e\n',
                     ' music_bands )asd ',
                     ' album_info_1976 a\n']

    def test_if_left_whitespace_is_removed(self):
        """
        test whitespace remove left site
        """
        expected_txt = "CREATE OR REPLACE VIEW abs  AS "
        cleaner = BaseSqlTextCleaner(text=self.__class__.test_sql_text)
        cleaner.rm_left_whitespace()
        self.assertEqual(cleaner.text, expected_txt)

    def test_remove_special_characters(self):
        """
        test if special characters can be removed
        """
        uncleaned_str = r"JOIN!\"#$%&'(HALLO)*+-/:<=>?@[\]^`{|}~"
        expected_txt = "JOINHALLO"
        cleaner = BaseSqlTextCleaner(text=uncleaned_str)
        cleaner.rm_special_characters()

        self.assertEqual(cleaner.text, expected_txt)

    def test_remove_linbreaks(self):
        """
        test if linebreaks can be removed
        """
        clean_text = []
        for word in self.__class__.test_str_list:
            cleaner = BaseSqlTextCleaner(text=word)
            cleaner.rm_linebreaks()
            clean_text.append(cleaner.text)

        clean_str = ''.join(clean_text)
        check = True
        if "\n" in clean_str:
            check = False
        self.assertEqual(check, True)

    def test_uppercase_String(self):
        """
        test if string uppercase works
        """
        expected_txt = "  CREATE OR REPLACE VIEW ABS  AS "
        cleaner = BaseSqlTextCleaner(text=self.__class__.test_sql_text)
        cleaner.uppercase_str()
        self.assertEqual(cleaner.text, expected_txt)


class TableSqlTextCleanerTest(unittest.TestCase):

    test_str_list = [' music_albums ',
                     ' CUSTOMERS,\nORDERS,\nPRODUCT\t',
                     ' old_join e\t',
                     ' music_bands )asd ',
                     ' album_info_1976 a\n']

    def test_remove_end_paranthesis(self):
        """
        test if everything after ) gets stripped
        """
        clean_text = []
        for word in self.__class__.test_str_list:
            cleaner = TableSqlTextCleaner(text=word)
            cleaner.rm_all_end_parenthesis()
            clean_text.append(cleaner.text)

        target_str = ''.join(clean_text)
        check = True
        if ")" in target_str:
            check = False

        self.assertEqual(check, True)

    def test_remove_tabs(self):
        """
        test if tabs can be removed from string
        """
        clean_text = []
        for word in self.__class__.test_str_list:
            cleaner = TableSqlTextCleaner(text=word)
            cleaner.rm_tabs()
            clean_text.append(cleaner.text)

        target_str = ''.join(clean_text)
        check = True
        if "\t" in target_str:
            check = False

        self.assertEqual(check, True)

    def test_start_method(self):
        """
        test main start method that runs all transformation
        """
        expected = ['MUSIC_ALBUMS',
                    'CUSTOMERS',
                    'ORDERS',
                    'PRODUCT',
                    'MUSIC_BANDS',
                    'OLD_JOIN',
                    'ALBUM_INFO_1976']

        clean_text = []
        for word in self.__class__.test_str_list:
            cleaner = TableSqlTextCleaner(text=word)
            cleaner.start()
            clean_text.append(cleaner.text)

        target_str = ''.join(clean_text)
        check = True
        for objekt in expected:
            if objekt in target_str:
                check = True
            else:
                check = False

        self.assertEqual(check, True)


if __name__ == "__main__":
    unittest.main()
