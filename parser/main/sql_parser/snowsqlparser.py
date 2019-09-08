import os
import re
from .sqlExpressions import reservedSqlExpressions, specialCharacters, endstatement
import exampleSql
from config.config_reader import Config

class ParseSql(object):
    def __init__(self, file):
        self.file = file
        self.filecontent = self.readFile()
        self.filename = os.path.basename(self.file)

    def readFile(self):
        with open(self.file ,encoding = 'utf-8') as f:
            return f.read()

    def UpperCaseContent(self):
        for element in reservedSqlExpressions:
            if element.lower() in self.filecontent:
                #print('##',element.lower(), '-->', element)
                #self.filecontent = self.filecontent.replace(element.lower(), element)
                self.filecontent = re.sub(r"\b"+ element.lower()+ r"\b", element, self.filecontent)

        #print(self.filecontent)
        return self
    
    def parseStatement(self, stat: str) -> list:
        statement = stat
        statementsFound = list()
        for m in re.finditer(statement, self.filecontent):
            #print('_found:',statement, m.start(), m.end())
            pos = {}
            pos['keyword'] = statement
            pos['startpos'] = m.start()
            pos['endpos']   = m.end()
            statementsFound.append(pos)
        return statementsFound

    def getCteNames(self):
        self.UpperCaseContent()
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
        #print(allkeywordPos)
        parsePair = list()
        for pos in self.parseStatement(stat='VIEW'):
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
            raw_str = self.removeLeftWhiteSpace(raw=raw_str)
            raw_str = self.removeAllWhiteSpaceFromString(raw=raw_str)
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
        startPositionsKeywords.sort()        
        return startPositionsKeywords

    def parseFromEnd(self):
        allkeywordPos = self.getParseNextAfterFrom()
        #print(allkeywordPos)
        parsePair = list()
        for pos in self.parseStatement(stat='FROM'):
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
            raw_str = self.removeAllAfterEndParenthesis(raw=raw_str)
            raw_str = self.removeSpecialCharacters(raw=raw_str)
            raw_str = self.removeLinebreaks(raw=raw_str)
            raw_str = self.removeLeftWhiteSpace(raw=raw_str)

            raw_str = self.detectOldJoin(raw=raw_str)
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
            #print('###', raw)
            raw = raw.lstrip()
            raw = raw.replace(" ", "")
            raw = raw.split(',')
            #print('###', raw)
        return raw

    def removeLeftWhiteSpace(self, raw: str) -> str:
        return raw.lstrip()
    
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
        tables =  [objekt for objekt in self.parseFromEnd() if objekt not in self.getCteNames()]
        objektName = None
        if self.getCreateName():
            objektName = self.getCreateName()
        return {'filename':self.filename, 'name':objektName, 'tables': tables}