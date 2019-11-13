# MIT License

# Copyright (c) 2019 Sebastian Daum

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

reservedSqlExpressions = [
    'WITH',
    'WHERE',
    'ALL',
    'ALTER',
    'AND',
    'ANY',
    'AS',
    'ASC',
    'BETWEEN',
    'BY',
    'CASE',
    'CAST',
    'CHECK',
    'CLUSTER',
    'COLUMN',
    'COMMENT'
    'CONNECT',
    'CREATE',
    'CROSS',
    'CURRENT_DATE',
    'CURRENT_ROLE',
    'CURRENT_USER',
    'CURRENT_TIME',
    'CURRENT_TIMESTAMP',
    'DELETE',
    'DESC',
    'DISTINCT',
    'DROP',
    'ELSE',
    'EXCLUSIVE',
    'EXISTS',
    'FALSE',
    'FOR',
    'FROM',
    'FULL',
    'GRANT',
    'GROUP',
    'HAVING',
    'IDENTIFIED',
    'ILIKE',
    'IMMEDIATE',
    'IN',
    'INCREMENT',
    'INNER',
    'INSERT',
    'INTERSECT',
    'INTO',
    'IS',
    'JOIN',
    'LATERAL',
    'LEFT',
    'LIKE',
    'LOCK',
    'LONG',
    'MAXEXTENTS',
    'MINUS',
    'MODIFY',
    'NATURAL',
    'NOT',
    'NULL',
    'OF',
    'ON',
    'OPTION',
    'OR',
    'ORDER',
    'REGEXP',
    'RENAME',
    'REVOKE',
    'RIGHT',
    'RLIKE',
    'ROW',
    'ROWS',
    'SAMPLE',
    'SELECT',
    'SET',
    'SOME',
    'START',
    'TABLE',
    'TABLESAMPLE',
    'THEN',
    'TO',
    'TRIGGER',
    'TRUE',
    'UNION',
    'UNIQUE',
    'UPDATE',
    'USING',
    'VALUES',
    'VIEW',
    'WHEN',
    'WHENEVER',
    'WHERE',
    'WITH'
    ]

endstatement = ';'

specialCharacters =  r"!\"#$%&'()*+-/:<=>?@[\]^`{|}~"

duallist = ['DUAL', 'dual']

technicalParameter = ['GFD', 'gfd']

