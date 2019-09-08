from main.sql_parser.snowsqlparser import ParseSql
from main.sql_parser.file_finder import FileFinder
from main.database.db_engine import Session
from main.database.models import TableDependency


class Runner(object):
    def __init__(self, allfiles=None):
        self.allfiles = None
        self.dependencies = list()

    def findFiles(self):
        return FileFinder().getListOfFiles()
    
    def parseSql(self):
        for file in self.allfiles:
            self.dependencies.append(ParseSql(file=file).getfinalFrom())

    def insertdep(self):
        session = Session()
        for sqlobject in self.dependencies:
            for table in sqlobject['tables']:
                dbentry = TableDependency( objectName = sqlobject['name'] ,
                                           filename = sqlobject['filename'],
                                           dependentTableName= table
                                        )
                session.add(dbentry)
                session.commit()
        session.close()


    def start(self):
        self.allfiles = self.findFiles()
        self.parseSql()
        self.insertdep()





