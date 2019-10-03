import os
import re
from .sqlExpressions import reservedSqlExpressions, specialCharacters, endstatement, duallist, technicalParameter
import exampleSql
from config.config_reader import Config
import textwrap

class ParseSql(object):
    def __init__(self, file):
        self.file = file
        self.filecontent = self.readFile()
        self.filename = os.path.basename(self.file)

    def readFile(self):
        with open(self.file ,encoding = 'utf-8') as f:
            return f.read()

    def UpperCaseContent(self):
        """
        Instance method that uppercase all keywords within the string
        """
        for element in reservedSqlExpressions:
            if element.lower() in self.filecontent:
                self.filecontent = re.sub(r"\b"+ element.lower()+ r"\b", element, self.filecontent)
        return self

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

    def debugger(self):
        self.base_clean_up()
        #self.remove_header_view_col_definition()
        #print(self.filecontent[95:1171])
        print(self.filecontent)
        #print(self.parseFromEnd())
        #print(self.getCreateName())

    def remove_header_view_col_definition(self):
        """
        Instance method checks there is a header column definition, It removes it if true.
        """
        firstline = self.filecontent.split('\n', 1)[0]

        if '(' in firstline:
            startpos= self.filecontent.find('(')
            endpos=   self.filecontent.find(')')
            #print(self.filecontent[startpos:endpos])

            self.filecontent = self.filecontent[:startpos] + self.filecontent[endpos+1:]

        #print(self.filecontent)

    def get_comma_cte_new_regex(self):
        #\w+(?=\s*(as|AS)[^/])
        pass

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
            allcommactes.append(raw)
        print(allcommactes)
        return allcommactes

    def unintend(self):
        data = self.filecontent.splitlines()
        new_list = list()

        for row in data:
            raw = self.removeLeftWhiteSpace(raw=row)
            raw = self.removeRightWhiteSpace(raw=raw)
            new_list.append(raw)
        self.filecontent = "\n".join(new_list)
        return "\n".join(new_list)

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
                allcommactes.append(raw)
        print(allcommactes)
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
        #print(parsePair)
        rawFroms = list()
        for pos in parsePair:
            start = pos[0]
            end   = pos[1]
            
            raw_str = self.filecontent[start:end]
            #print('1', raw_str)
            raw_str = self.removeAllAfterEndParenthesis(raw=raw_str)
            #print('2', raw_str)
            raw_str = self.removeSpecialCharacters(raw=raw_str)
            #print('3', raw_str)
            raw_str = self.removeLinebreaks(raw=raw_str)
            #print('4', raw_str)
            raw_str = self.removeLeftWhiteSpace(raw=raw_str)
            #print('5', raw_str)

            #print(">>>>>>>>>>>>>>>", raw_str)

            #raw_str = self.detectOldJoin(raw=raw_str)
            if isinstance(raw_str, list):
                rawFroms.extend(raw_str)
            else:
                rawFroms.append(raw_str)

        rawFroms = self.removeAllAfterWhitespace(raw=rawFroms)
        return rawFroms

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
            if char in raw:
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
            print('$$$$$ There is a comma in a string:', raw)
            print('###', raw)
            raw = raw.lstrip()
            raw = raw.replace(" ", "")
            raw = raw.split(',')
            #print('###', raw)
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

    def remove_comments(self):
        """ remove c-style comments.
            text: blob of text with comments (can include newlines)
            returns: text with comments removed
        """
        self.filecontent = re.sub('\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$', '', self.filecontent )
        self.filecontent = re.sub('--.*?\n', '', self.filecontent )
        #return re.sub('\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$', '', raw)

    def getfinalFrom(self):
        self.base_clean_up()

        tables =  [objekt for objekt in self.parseFromEnd() if objekt not in self.getCteNames() 
                                                                      and objekt not in duallist
                                                                      and objekt not in self.parseCommaCTEs()
                                                                      and objekt not in self.newparseCommaCTEs()
                                                                      and objekt not in self.detect_next_line_as()   
                                                                      and objekt not in technicalParameter  
                                                                    ]
        tables = [self.upperStr(raw=table) for table in tables]
                                                                      
        objektName = None
        if self.getCreateName():
            objektName = self.getCreateName()
            objektName = self.upperStr(objektName)
        print( {'filename':self.filename, 'name':objektName, 'tables': tables} )
        print( '-------------------------------')
        return {'filename':self.filename, 'name':objektName, 'tables': tables}