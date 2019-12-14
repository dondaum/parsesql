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

import os
import re
from .sqlExpressions import reservedSqlExpressions, specialCharacters, endstatement, duallist, technicalParameter
from util.logger_service import LoggerMixin
import exampleSql
import textwrap

class ParseSql(LoggerMixin):
    def __init__(self, file):
        self.file = file
        self.filecontent = self._readFile()
        self.filename = os.path.basename(self.file)

        self._base_clean_up()
        self.allkeywordPos  = self._getParseNextAfterFrom()

    def _readFile(self) -> str:
        with open(self.file ,encoding = 'utf-8') as f:
            return f.read()

    def _base_clean_up(self) -> None:
        """
        this method calls base instance method that prepare the file content for parsing
        """
        # instance method that removes comments
        self._remove_comments()
        # instance method that uppercase all keywords
        self._uppercase_sql_expressions()
        # instance method that removes the left and right indention
        self._unintend()
        # remove view header
        self._remove_header_view_col_definition()
        # lstrip UNSTABLE
        self._lstrip()

    def _remove_comments(self) -> None:
        """ remove c-style comments.
            text: blob of text with comments (can include newlines)
            returns: text with comments removed
        """
        self.filecontent = re.sub('\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$', '', self.filecontent )
        self.filecontent = re.sub('--.*?\n', '', self.filecontent )

    def _uppercase_sql_expressions(self) -> None:
        """
        Instance method that uppercase all keywords within the string
        """
        for element in reservedSqlExpressions:
            if element.lower() in self.filecontent:
                self.filecontent = re.sub(r"\b"+ element.lower()+ r"\b", element, self.filecontent)

    def _unintend(self) -> None:
        """
        Instance method standardize the intend of the file
        """
        data = self.filecontent.splitlines()
        new_list = list()
        for row in data:
            cleaned_text = LigthSqlTextCleaner(text=row).start()
            new_list.append(cleaned_text)
        self.filecontent = "\n".join(new_list)

    def _remove_header_view_col_definition(self):
        """
        Instance method checks there is a header column definition, It removes it if true.
        """
        firstline = self.filecontent.split('\n', 1)[0]

        if '(' in firstline:
            startpos= self.filecontent.find('(')
            endpos=   self.filecontent.find(')')
            self.filecontent = self.filecontent[:startpos] + self.filecontent[endpos+1:]
    
    def _lstrip(self) -> None:
        """
        Instance method for lstrip
        """
        self.filecontent.lstrip()

    def _get_cte_names(self) -> list:
        allcommactes = list()
        for cte in re.finditer(r"\w+(?=\s*(\bas\b|\bAS\b)[^/])", self.filecontent, re.MULTILINE):
            raw = cte.group(0)
            allcommactes.append(CTESqlTextCleaner(text=raw).start())
        return allcommactes

    def _parse_statement(self, stat: str) -> list:
        statement = stat
        statementsFound = list()
        for m in re.finditer(r"\b"+ statement + r"\b", self.filecontent):
            pos = {}
            pos['keyword'] = statement
            pos['startpos'] = m.start()
            pos['endpos']   = m.end()
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
            end   = pos[1]
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
        parsePair = parsePair[:1] # only take first two positions
        raw_str = ''
        for pos in parsePair:
            start = pos[0]
            end   = pos[1]
            raw_str = self.filecontent[start:end]
        return CreateSqlTextCleaner(text=raw_str).start()

    def _getParseNextAfterFrom(self) -> list:
        startPositionsKeywords = list()
        for keyword in reservedSqlExpressions:
            for m in re.finditer(r"\b"+ keyword + r"\b", self.filecontent):
                startPositionsKeywords.append(m.start())
        for stat in endstatement:
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
        allkeywordPos = self.allkeywordPos
        parsePair = list()
        keywordlist = ['FROM', 'JOIN']
        for searchkey in keywordlist:
            for pos in self._parse_statement(stat=searchkey):
                for allpos in allkeywordPos:
                    if pos['endpos'] < allpos:
                        parsePair.append([pos['endpos'], allpos])
                        break
        rawFroms = list()
        for pos in parsePair:
            start = pos[0]
            end   = pos[1]
            
            raw_str = self.filecontent[start:end]
            cleaned_text = TableSqlTextCleaner(text=raw_str).start()
            cleaned_text = self._detectOldJoin(raw=cleaned_text)

            if isinstance(cleaned_text, list):
                rawFroms.extend(cleaned_text)
            else:
                cleaned_text = self.removeCommaCharacters(raw=cleaned_text)
                rawFroms.append(cleaned_text)

        rawFroms = self._removeAllAfterWhitespace(raw=rawFroms)
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
            final_raw = list()
            for e in raw:
                e = e.lstrip()
                final_raw.append(e)
            return final_raw
        return raw

    def _removeAllAfterWhitespace(self, raw: list) -> list:
        whitespace = ' '
        newraw = list() 
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
        tables =  [objekt for objekt in self._parseFromEnd() if objekt not in self._get_with_name() 
                                                                      and objekt not in self._get_cte_names()
                                                                      and objekt not in duallist 
                                                                      and objekt not in technicalParameter  
                                                                    ]                                                         
        if self._get_create_name():
            objektName = self._get_create_name()
        final_dict = {'filename':self.filename, 'name':objektName, 'tables': tables}
        self.logger.info(f'Parsing of a file completed: {final_dict}')
        return final_dict


class BaseSqlTextCleaner(object):
    
    def removeSpecialCharacters(self) -> None:
        for char in specialCharacters:
            if char in self.text:
                self.text = self.text.replace(char, '')
    
    def removeCommaCharacters(self) -> None:
        char = ','
        if char in self.text:
            self.text = self.text.replace(char, '')
    
    def removeLeftWhiteSpace(self) -> str:
        self.text = self.text.lstrip()

    def upperStr(self) -> None:
        self.text = self.text.upper()

    def removeAllWhiteSpaceFromString(self) -> None:
        whitespace = ' '
        if whitespace in self.text:
            pos = self.text.find(whitespace)
            self.text = self.text[:pos]
    
    def removeLinebreaks(self) -> None:
        self.text = self.text.replace('\n','')

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
        self.removeLeftWhiteSpace()
        self.removeRightWhiteSpace()
        return self.text

    def removeRightWhiteSpace(self) -> str:
        self.text = self.text.rstrip()

class TableSqlTextCleaner(BaseSqlTextCleaner):
    
    def __init__(self, text: str):
        self.text = text

    def start(self) -> str:
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeAllAfterEndParenthesis()
        self.removeSpecialCharacters()
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
        self.removeSpecialCharacters()
        self.removeCommaCharacters()
        self.removeReservedCharacters()
        self.removeLeftWhiteSpace()
        self.removeAllWhiteSpaceFromString()
        self.upperStr()
        return self.text

    def removeReservedCharacters(self) -> None:
        for char in reservedSqlExpressions:
            if re.match(r"\b"+ char + r"\b", self.text):
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



    