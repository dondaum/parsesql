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
from parsesql.main.sql_parser import sqlExpressions


class SqlExpressionTest(unittest.TestCase):

    def test_if_all_global_variables_exist(self):
        """
        test if all sql expressions global variable exist
        """
        PARAMS = [
            "RESERVED_SQL_EXPRESSIONS",
            "END_STATEMENT",
            "SPECIAL_CHARACTERS",
            "DUAL_LIST",
            "TECHNICAL_PARAM",
        ]
        module_variables = dir(sqlExpressions)
        all_var_exist = True
        for param in PARAMS:
            if param not in module_variables:
                all_var_exist = False

        self.assertEqual(True, all_var_exist)


if __name__ == "__main__":
    unittest.main()
