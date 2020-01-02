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

import os
import re
from .sqlExpressions import (RESERVED_SQL_EXPRESSIONS,
                             SPECIAL_CHARACTERS,
                             END_STATEMENT,
                             DUAL_LIST,
                             TECHNICAL_PARAM
                             )
from parsesql.util.logger_service import LoggerMixin
from typing import Generator


class ParseSql(LoggerMixin):
    def __init__(self, file):
        self.file = file
        self.filecontent = self._readFile()
        self.filename = os.path.basename(self.file)

        self._base_clean_up()
        self.allkeywordPos = self._get_keyword_positions()

    def _readFile(self) -> str:
        with open(self.file, encoding='utf-8') as f:
            return f.read()

    def _base_clean_up(self) -> None:
        """
        this method calls base instance method that prepare the file content
        for parsing
        """
        self._remove_comments() \
            ._uppercase_sql_expressions() \
            ._unintend() \
            ._remove_header_view_col_definition() \
            ._remove_empty_lines()

    def _remove_comments(self) -> None:
        """
        remove c-style comments.
        text: blob of text with comments (can include newlines)
        returns: text with comments removed
        """
        # TODO: Check if r escaping works as expected
        self.filecontent = re.sub(r'\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$',
                                  '', self.filecontent)
        self.filecontent = re.sub('--.*?\n', '', self.filecontent)
        return self

    def _uppercase_sql_expressions(self) -> None:
        """
        Instance method that uppercase all keywords within the string
        """
        for element in self._consume_reserved_sql_combinations():
            if element in self.filecontent:
                self.filecontent = re.sub(r"\b" + element + r"\b",
                                          element.upper(), self.filecontent)
        return self

    def _get_all_reserved_sql_combinations(self, s: str
                                           ) -> Generator[str, None, None]:
        """
        Instance method that returns a generator for all possible string
        combinations
        """
        if s == '':
            yield ''
            return
        for rest in self._get_all_reserved_sql_combinations(s[1:]):
            yield s[0].upper() + rest
            if s[0].upper() != s[0].lower():
                yield s[0].lower() + rest

    def _consume_reserved_sql_combinations(self
                                           ) -> Generator[str, None, None]:
        """
        Instance method that creates all SQL combination and retunrs
        them as a generator
        """
        for sql_keyword in RESERVED_SQL_EXPRESSIONS:
            yield from self._get_all_reserved_sql_combinations(s=sql_keyword)

    def _unintend(self) -> None:
        """
        Instance method standardize the intend of the file by removing left
        and right space
        """
        data = self.filecontent.splitlines()
        new_list = []
        for row in data:
            cleaned_text = LigthSqlTextCleaner(text=row).start()
            new_list.append(cleaned_text)
        self.filecontent = "\n".join(new_list)
        return self

    def _remove_header_view_col_definition(self):
        """
        Instance method checks there is a header column definition, It removes
        it if true.
        """
        splitted_content = self.filecontent.splitlines()

        line = 0
        while True:
            firstline = splitted_content[line]
            if (firstline.isspace() or len(firstline) <= 0):
                line += 1
            else:
                break

        if '(' in firstline:
            startpos = self.filecontent.find('(')
            endpos = self.filecontent.find(')')
            self.filecontent = (self.filecontent[:startpos] +
                                self.filecontent[endpos+1:])
        return self

    def _remove_empty_lines(self):
        """
        Instance method that removes empty lines from string
        """
        splitted_content = self.filecontent.splitlines()
        for idx, line in enumerate(splitted_content):
            if (line.isspace() or len(line) <= 0):
                del splitted_content[idx]

        self.filecontent = "\n".join(splitted_content)
        return self

    def _get_cte_names(self) -> list:
        allcommactes = list()
        for cte in re.finditer(r"\w+(?=\s*(\bas\b|\bAS\b)[^/])",
                               self.filecontent,
                               re.MULTILINE):
            raw = cte.group(0)
            allcommactes.append(CTESqlTextCleaner(text=raw).start())
        return allcommactes

    def _get_recursive_cte_names(self) -> list:
        allrec = []
        for cte in re.finditer(r"^\,(?:.*)(\n?\($)",
                               self.filecontent,
                               re.MULTILINE):
            raw = cte.group(0)
            allrec.append(RecursiveSqlTextCleaner(text=raw).start())
        return allrec

    def _parse_statement(self, stat: str) -> list:
        """
        Instance method that searches for a certain substring and returns
        a list if keyword and start and end position
        """
        statement = stat
        statementsFound = []
        for m in re.finditer(r"\b" + statement + r"\b", self.filecontent):
            pos = {}
            pos['keyword'] = statement
            pos['startpos'] = m.start()
            pos['endpos'] = m.end()
            statementsFound.append(pos)
        return statementsFound

    def _get_with_name(self):
        allkeywordPos = self.allkeywordPos
        parsePair = list()
        for pos in self._parse_statement(stat='WITH'):
            for allpos in allkeywordPos:
                if pos['endpos'] < allpos:
                    parsePair.append([pos['endpos'], allpos])
                    break
        raw_str = ''
        for pos in parsePair:
            start = pos[0]
            end = pos[1]
            raw_str = self.filecontent[start:end]
            raw_str = raw_str.replace(" ", "")
        return raw_str

    def _get_create_name(self):
        allkeywordPos = self.allkeywordPos
        parsePair = list()
        for pos in self._parse_statement(stat='VIEW'):
            for allpos in allkeywordPos:
                if pos['endpos'] < allpos:
                    parsePair.append([pos['endpos'], allpos])
                    break
        # only take first two positions
        parsePair = parsePair[:1]
        raw_str = ''
        for pos in parsePair:
            start = pos[0]
            end = pos[1]
            raw_str = self.filecontent[start:end]
        return CreateSqlTextCleaner(text=raw_str).start()

    def _get_keyword_positions(self) -> list:
        """
        Instance method that gets all coordinates for reserved keywords if
        available. It also adds an end keyword if no end keyword found
        """
        startPositionsKeywords = []
        for keyword in RESERVED_SQL_EXPRESSIONS:
            for m in re.finditer(r"\b" + keyword + r"\b", self.filecontent):
                startPositionsKeywords.append(m.start())
        for stat in END_STATEMENT:
            if stat in self.filecontent:
                pos = self.filecontent.find(stat)
                startPositionsKeywords.append(pos)
            else:
                self.filecontent = self.filecontent + stat
                pos = self.filecontent.find(stat)
                startPositionsKeywords.append(pos)

        startPositionsKeywords.sort()
        return startPositionsKeywords

    def _parseFromEnd(self) -> list:
        """
        Instance method that returns the final FROM and JOIN object
        reference results
        """
        rawFroms = []
        raw_dependencies = self._parse_uncleaned_text()

        for dependency in raw_dependencies:
            cleaned_text = TableSqlTextCleaner(text=dependency).start()
            cleaned_text = self._detectOldJoin(raw=cleaned_text)

            if isinstance(cleaned_text, list):
                rawFroms.extend(cleaned_text)
            else:
                cleaned_text = self.removeCommaCharacters(raw=cleaned_text)
                rawFroms.append(cleaned_text)

        rawFroms = self._removeAllAfterWhitespace(raw=rawFroms)
        return rawFroms

    def _parse_position_pair(self) -> list:
        """
        Instance method that parse the keyword pair positions
        """
        allkeywordPos = self.allkeywordPos
        parsePair = []
        keywordlist = ['FROM', 'JOIN']
        for searchkey in keywordlist:
            for pos in self._parse_statement(stat=searchkey):
                for allpos in allkeywordPos:
                    if pos['endpos'] < allpos:
                        parsePair.append([pos['endpos'], allpos])
                        break
        return parsePair

    def _parse_uncleaned_text(self) -> list:
        """
        Instance method that parses raw substrings after JOIN and FROM
        """
        parsePair = self._parse_position_pair()
        rawFroms = []
        for pos in parsePair:
            start, end = pos[0], pos[1]
            rawFroms.append(self.filecontent[start:end])
        return rawFroms

    def removeCommaCharacters(self, raw: str) -> str:
        """
        TODO: Refactor the _parseFromEnd method in order to apply DRY
        """
        char = ','
        if char in raw:
            raw = raw.replace(char, '')
        return raw

    def _detectOldJoin(self, raw: str) -> list:
        comma = ','
        if comma in raw:
            raw = raw.lstrip()
            raw = raw.split(',')
            final_raw = []
            for e in raw:
                e = e.lstrip()
                final_raw.append(e)
            return final_raw
        return raw

    def _removeAllAfterWhitespace(self, raw: list) -> list:
        whitespace = ' '
        newraw = []
        for element in raw:
            if whitespace in element:
                pos = element.find(whitespace)
                element = element[:pos]
                newraw.append(element)
            else:
                newraw.append(element)
        return newraw

    def getfinalFrom(self) -> dict:
        objektName = None
        tables = [objekt for objekt in self._parseFromEnd()
                  if objekt not in self._get_with_name()
                  and objekt not in self._get_cte_names()
                  and objekt not in self._get_recursive_cte_names()
                  and objekt not in DUAL_LIST
                  and objekt not in TECHNICAL_PARAM]

        if self._get_create_name():
            objektName = self._get_create_name()
        final_dict = {'filename': self.filename,
                      'name': objektName,
                      'tables': tables}

        self.logger.info(f'Parsing of a file completed: {final_dict}')
        return final_dict


class BaseSqlTextCleaner(object):

    def __init__(self, text: str):
        self.text = text

    def removeSPECIAL_CHARACTERS(self) -> None:
        for char in SPECIAL_CHARACTERS:
            if char in self.text:
                self.text = self.text.replace(char, '')

    def removeCommaCharacters(self) -> None:
        char = ','
        if char in self.text:
            self.text = self.text.replace(char, '')

    def removeLeftWhiteSpace(self) -> str:
        self.text = self.text.lstrip()
        return self

    def upperStr(self) -> None:
        self.text = self.text.upper()

    def removeAllWhiteSpaceFromString(self) -> None:
        whitespace = ' '
        if whitespace in self.text:
            pos = self.text.find(whitespace)
            self.text = self.text[:pos]

    def removeLinebreaks(self) -> None:
        self.text = self.text.replace('\n', '')

    def removeAllAfterStartParenthesis(self) -> None:
        """
        String mehtod that removes all characters after the opening paranthesis
        """
        paranthesis = '('
        if paranthesis in self.text:
            pos = self.text.find(paranthesis)
            self.text = self.text[:pos]


class LigthSqlTextCleaner(BaseSqlTextCleaner):

    def __init__(self, text: str):
        self.text = text

    def start(self):
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeLeftWhiteSpace().removeRightWhiteSpace()
        return self.text

    def removeRightWhiteSpace(self) -> str:
        self.text = self.text.rstrip()
        return self


class TableSqlTextCleaner(BaseSqlTextCleaner):

    def __init__(self, text: str):
        self.text = text

    def start(self) -> str:
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeAllAfterEndParenthesis()
        self.removeSPECIAL_CHARACTERS()
        self.removeLinebreaks()
        self.removeLeftWhiteSpace()
        self.removeTabs()
        self.upperStr()
        return self.text

    def removeTabs(self) -> str:
        """
        instance method that replace tabs character with whitespace
        """
        self.text = self.text.replace('\t', ' ')

    def removeAllAfterEndParenthesis(self) -> None:
        paranthesis = ')'
        if paranthesis in self.text:
            pos = self.text.find(paranthesis)
            self.text = self.text[:pos]


class CTESqlTextCleaner(BaseSqlTextCleaner):

    def __init__(self, text: str):
        self.text = text

    def start(self) -> str:
        """
        Main control method that starts text cleaning and transforming
        """
        self.remove_whitespace()
        self.removeSPECIAL_CHARACTERS()
        self.removeCommaCharacters()
        self.removeReservedCharacters()
        self.removeLeftWhiteSpace()
        self.removeAllWhiteSpaceFromString()
        self.upperStr()
        return self.text

    def removeReservedCharacters(self) -> None:
        for char in RESERVED_SQL_EXPRESSIONS:
            if re.match(r"\b" + char + r"\b", self.text):
                self.text = self.text.replace(char, '')

    def remove_whitespace(self) -> None:
        self.text = self.text.replace(" ", "")


class CreateSqlTextCleaner(BaseSqlTextCleaner):

    def __init__(self, text: str):
        self.text = text

    def start(self) -> str:
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeLeftWhiteSpace()
        self.removeAllWhiteSpaceFromString()
        self.removeLinebreaks()
        self.removeAllAfterStartParenthesis()
        self.upperStr()
        return self.text


class RecursiveSqlTextCleaner(BaseSqlTextCleaner):

    def __init__(self, text: str):
        self.text = text

    def removeAllAfterAs(self) -> None:
        expr = ' AS'
        if expr in self.text:
            pos = self.text.find(expr)
            self.text = self.text[:pos]

    def start(self) -> str:
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeAllAfterAs()
        self.removeAllAfterStartParenthesis()
        self.removeCommaCharacters()
        self.removeLeftWhiteSpace()
        self.removeAllWhiteSpaceFromString()
        self.upperStr()
        return self.text
