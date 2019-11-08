import os
import re
from .sqlExpressions import reservedSqlExpressions, specialCharacters, endstatement, duallist, technicalParameter
from util.logger_service import LoggerMixin
import exampleSql
import textwrap

class ParseSql(LoggerMixin):
    def __init__(self, file):
        self.file = file
        self.filecontent = self.readFile()
        self.filename = os.path.basename(self.file)

    def readFile(self):
        with open(self.file ,encoding = 'utf-8') as f:
            return f.read()

    def base_clean_up(self):
        """
        this method calls base instance method that prepare the file content for parsing
        """
        # instance method that removes comments
        self.remove_comments()
        # instance method that uppercase all keywords
        self.UpperCaseContent()
        # instance method that removes the left and right indention
        self.unintend()
        # remove view header
        self.remove_header_view_col_definition()

    def remove_comments(self):
        """ remove c-style comments.
            text: blob of text with comments (can include newlines)
            returns: text with comments removed
        """
        self.filecontent = re.sub('\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$', '', self.filecontent )
        self.filecontent = re.sub('--.*?\n', '', self.filecontent )

    def UpperCaseContent(self):
        """
        Instance method that uppercase all keywords within the string
        """
        for element in reservedSqlExpressions:
            if element.lower() in self.filecontent:
                self.filecontent = re.sub(r"\b"+ element.lower()+ r"\b", element, self.filecontent)

    def unintend(self):
        """
        Instance method standardize the intend
        """
        data = self.filecontent.splitlines()
        new_list = list()
        for row in data:
            cleaned_text = BaseSqlTextCleaner(text=row).start()
            new_list.append(cleaned_text)
        self.filecontent = "\n".join(new_list)
        return "\n".join(new_list)

    def remove_header_view_col_definition(self):
        """
        Instance method checks there is a header column definition, It removes it if true.
        """
        firstline = self.filecontent.split('\n', 1)[0]

        if '(' in firstline:
            startpos= self.filecontent.find('(')
            endpos=   self.filecontent.find(')')
            self.filecontent = self.filecontent[:startpos] + self.filecontent[endpos+1:]

    def debugger(self):
        self.base_clean_up()
        #self.remove_header_view_col_definition()
        #print(self.filecontent[95:1171])
        #print(self.filecontent)
        self.getfinalFrom()
        #print(self.get_comma_cte_new_regex())
        #print(self.parseFromEnd())
        #print(self.getCreateName())

    def get_comma_cte_new_regex(self):
        #\w+(?=\s*(as|AS)[^/])
        #\w+(?=\s*(\bas\b|\bAS\b)[^/])
        #(?<=\AS\s)(\w+)
        #\w+(?=\s+AS)
        
        allcommactes = list()

        for cte in re.finditer(r"\w+(?=\s*(\bas\b|\bAS\b)[^/])", self.filecontent, re.MULTILINE):
            raw = cte.group(0)
            raw = raw.replace(" ", "")
            raw = self.removeSpecialCharacters(raw=raw)
            raw = self.removeCommaCharacters(raw=raw)
            raw = self.removeReservedCharacters(raw=raw)
            #print(raw)
            raw = self.removeLeftWhiteSpace(raw=raw)
            raw = self.removeAllWhiteSpaceFromString(raw=raw)
            raw = raw.upper()
            #print(raw)
            allcommactes.append(raw)
        return allcommactes

    def parseStatement(self, stat: str) -> list:
        statement = stat
        statementsFound = list()
        for m in re.finditer(r"\b"+ statement + r"\b", self.filecontent):
            #print('_found:',statement, m.start(), m.end())
            pos = {}
            pos['keyword'] = statement
            pos['startpos'] = m.start()
            pos['endpos']   = m.end()
            statementsFound.append(pos)
        return statementsFound

    def parseCommaCTEs(self) -> list:
        self.UpperCaseContent()
        # ^,.*+AS$
        # (^,.*)+(AS{1,2})
        #(^,.*)+(AS{1,2}$)
        #(^,.*)(AS$|as$|\()
        # x = re.findall(r"(^,.*)(AS{1,2}$)", self.filecontent, re.MULTILINE)
        # print(x)
        allcommactes = list()

        for cte in re.finditer(r"(^,.*)(AS{1,2}$|\($)", self.filecontent, re.MULTILINE):
            raw = cte.group(0)
            raw = self.removeSpecialCharacters(raw=raw)
            raw = self.removeCommaCharacters(raw=raw)
            raw = self.removeReservedCharacters(raw=raw)
            raw = self.removeLeftWhiteSpace(raw=raw)
            raw = self.removeAllWhiteSpaceFromString(raw=raw)
            raw = raw.upper()
            allcommactes.append(raw)
        #print(allcommactes)
        return allcommactes

    def detect_next_line_as(self):
        self.unintend()
        data = self.filecontent.splitlines()
        allcommactes = list()

        for row in data:
            if row.startswith('AS'):
                current_index = data.index(row)
                raw = data[ current_index -1 ]
                raw = self.removeSpecialCharacters(raw=raw)
                raw = self.removeCommaCharacters(raw=raw)
                raw = self.removeReservedCharacters(raw=raw)
                raw = self.removeLeftWhiteSpace(raw=raw)
                raw = self.removeAllWhiteSpaceFromString(raw=raw)
                raw = raw.upper()
                allcommactes.append(raw)
        #print(allcommactes)
        return allcommactes

    def newparseCommaCTEs(self):
        self.UpperCaseContent()
        allcommactes = list()
        self.remove_comments()
        expectend_ends = ['(','']
        self.filecontent.lstrip()

        #print(self.filecontent)

        allcommactes = list()

        for cte in re.finditer(r"(^,.*)(AS$|\($|AS.*\n)", self.filecontent, re.MULTILINE):
            raw = cte.group(0)
            raw = raw.replace(" ", "")
            #print(raw)
            if raw.endswith("\n"):
                raw = raw.strip()
                #print(raw)
                if raw.split("AS",1)[1] in expectend_ends:
                    #print(next_str)
                    raw = self.removeSpecialCharacters(raw=raw)
                    raw = self.removeCommaCharacters(raw=raw)
                    raw = self.removeReservedCharacters(raw=raw)
                    raw = self.removeLeftWhiteSpace(raw=raw)
                    raw = self.removeAllWhiteSpaceFromString(raw=raw)
                    raw = raw.upper()
                    #print(raw)
                    allcommactes.append(raw)
        #print(allcommactes)
        return allcommactes

    def getCteNames(self):
        allkeywordPos = self.getParseNextAfterFrom()
        parsePair = list()
        for pos in self.parseStatement(stat='WITH'):
            for allpos in allkeywordPos:
                if pos['endpos'] < allpos:
                    parsePair.append([pos['endpos'], allpos])
                    break
        #print(parsePair)
        raw_str = ''
        for pos in parsePair:
            start = pos[0]
            end   = pos[1]
            raw_str = self.filecontent[start:end]
            raw_str = raw_str.replace(" ", "")
        return raw_str

    def getCreateName(self):
        self.UpperCaseContent()
        #print(self.filecontent)
        allkeywordPos = self.getParseNextAfterFrom()
        self.remove_comments()
        #print(allkeywordPos)
        parsePair = list()
        for pos in self.parseStatement(stat='VIEW'):
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
            raw_str = self.removeLeftWhiteSpace(raw=raw_str)
            raw_str = self.removeAllWhiteSpaceFromString(raw=raw_str)
            raw_str = self.removeLinebreaks(raw=raw_str)
        return raw_str

    def getParseNextAfterFrom(self):
        self.UpperCaseContent()
        #print('1:', self.filecontent)
        startPositionsKeywords = list()
        for keyword in reservedSqlExpressions:
            #print('searched keywords, ', keyword)
            for m in re.finditer(r"\b"+ keyword + r"\b", self.filecontent):
                #print('found keyword', keyword)
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

    def parseFromEnd(self):
        allkeywordPos = self.getParseNextAfterFrom()
        #print(allkeywordPos)
        parsePair = list()
        keywordlist = ['FROM', 'JOIN']
        for searchkey in keywordlist:
            for pos in self.parseStatement(stat=searchkey):
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
            #print(">>>>>>>>>>>>>>>", cleaned_text)
            cleaned_text = self.detectOldJoin(raw=cleaned_text)

            if isinstance(cleaned_text, list):
                rawFroms.extend(cleaned_text)
            else:
                cleaned_text = self.removeCommaCharacters(raw=cleaned_text)
                rawFroms.append(cleaned_text)

        rawFroms = self.removeAllAfterWhitespace(raw=rawFroms)
        #print('99', rawFroms)
        return rawFroms

    def removeTabs(self, raw: str) -> str:
        """
        instance method that replace tabs character with whitespace
        """
        return raw.replace('\t', ' ')

    def removeLinebreaks(self, raw: str) -> str:
        return raw.replace('\n','')
        #return [ newstr.replace(' ', '') for newstr in raw ]

    def removeSpecialCharacters(self, raw: str) -> str:
        for char in specialCharacters:
            if char in raw:
                #print('Character found: ', char)
                raw = raw.replace(char, '')
        return raw
    
    def removeCommaCharacters(self, raw: str) -> str:
        char = ','
        if char in raw:
            raw = raw.replace(char, '')
        return raw

    def removeReservedCharacters(self, raw: str) -> str:
        for char in reservedSqlExpressions:
            #if char in raw:
            if re.match(r"\b"+ char + r"\b", raw):
                #print('Character found: ', char)
                raw = raw.replace(char, '')
        return raw

    def removeAllAfterEndParenthesis(self, raw: str) -> str:
        paranthesis = ')'
        if paranthesis in raw:
            pos = raw.find(paranthesis)
            raw = raw[:pos]
            #print('position is:', pos)
        return raw

    def detectOldJoin(self, raw: str) -> list:
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

    def removeLeftWhiteSpace(self, raw: str) -> str:
        return raw.lstrip()
    
    def removeRightWhiteSpace(self, raw: str) -> str:
        return raw.rstrip()

    def upperStr(self, raw: str) -> str:
        return raw.upper()
    
    def removeAllWhiteSpaceFromString(self, raw: str) -> str:
        whitespace = ' '
        if whitespace in raw:
            pos = raw.find(whitespace)
            #print('whitespace detected', pos)
            return raw[:pos]
        else:
            return raw

    def removeAllWhiteSpaceFromList(self, raw: str) -> str:
        return [s.replace(" ", "") for s in raw]

    def removeAllAfterWhitespace(self, raw: list) -> list:
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


    def getfinalFrom(self):
        self.base_clean_up()

        tables =  [objekt for objekt in self.parseFromEnd() if objekt not in self.getCteNames() 
                                                                      and objekt not in duallist
                                                                      and objekt not in self.parseCommaCTEs()
                                                                      and objekt not in self.newparseCommaCTEs()
                                                                      and objekt not in self.detect_next_line_as()   
                                                                      and objekt not in technicalParameter  
                                                                      and objekt not in self.get_comma_cte_new_regex()
                                                                    ]
        tables = [self.upperStr(raw=table) for table in tables]
                                                                      
        objektName = None
        if self.getCreateName():
            objektName = self.getCreateName()
            objektName = self.upperStr(objektName)
        #print( {'filename':self.filename, 'name':objektName, 'tables': tables} )
        #print( '-------------------------------')
        final_dict = {'filename':self.filename, 'name':objektName, 'tables': tables}
        self.logger.info(f'Parsing of a file completed: {final_dict}')
        return final_dict

class BaseSqlTextCleaner(object):

    def __init__(self, text: str):
        self.text = text

    def start(self):
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeLeftWhiteSpace()
        self.removeRightWhiteSpace()
        return self.text

    def removeLeftWhiteSpace(self) -> str:
        self.text = self.text.lstrip()

    def removeRightWhiteSpace(self) -> str:
        self.text = self.text.rstrip()


class TableSqlTextCleaner(BaseSqlTextCleaner):
    
    def __init__(self, text: str):
        self.text = text

    def start(self):
        """
        Main control method that starts text cleaning and transforming
        """
        self.removeAllAfterEndParenthesis()
        #print('1', self.text)
        self.removeSpecialCharacters()
        #print('2', self.text)
        self.removeLinebreaks()
        #print('3', self.text)
        self.removeLeftWhiteSpace()
        #print('4', self.text)
        self.removeTabs()
        #print('5', self.text)
        self.upperStr()
        #print('6', self.text)
        return self.text

    def removeTabs(self) -> str:
        """
        instance method that replace tabs character with whitespace
        """
        self.text = self.text.replace('\t', ' ')

    def removeLinebreaks(self) -> None:
        self.text = self.text.replace('\n','')

    def removeSpecialCharacters(self) -> None:
        for char in specialCharacters:
            if char in self.text:
                #print('Character found: ', char)
                self.text = self.text.replace(char, '')
    
    def removeCommaCharacters(self) -> None:
        char = ','
        if char in self.text:
            self.text = self.text.replace(char, '')

    def removeReservedCharacters(self) -> None:
        for char in reservedSqlExpressions:
            #if char in raw:
            if re.match(r"\b"+ char + r"\b", self.text):
                #print('Character found: ', char)
                self.text = self.text.replace(char, '')

    def removeAllAfterEndParenthesis(self) -> None:
        paranthesis = ')'
        if paranthesis in self.text:
            pos = self.text.find(paranthesis)
            self.text = self.text[:pos]
    
    def upperStr(self) -> None:
        self.text = self.text.upper()



    