from main.sql_parser.snowsqlparser import ParseSql
from main.sql_parser.file_finder import FileFinder
from main.database.db_engine import Session
from main.database.models import TableDependency
import uuid


class Runner(object):
    def __init__(self):
        self.allfiles = None
        self.dependencies = list()

    def findFiles(self):
        self.allfiles = FileFinder().getListOfFiles()
    
    def parseSql(self):
        for file in self.allfiles:
            self.dependencies.append(ParseSql(file=file).getfinalFrom())

    def unitendtest(self):
        #unintend
        for file in self.allfiles:
            #ParseSql(file=file).parseCommaCTEs()
            ParseSql(file=file).debugger()
    
    def parseCTE(self):
        for file in self.allfiles:
            #ParseSql(file=file).parseCommaCTEs()
            ParseSql(file=file).newparseCommaCTEs()

    def parseCreateName(self):
        for file in self.allfiles:
            ParseSql(file=file).getCreateName()

    def insertdep(self):
        session = Session()
        for sqlobject in self.dependencies:
            for table in sqlobject['tables']:
                dbentry = TableDependency( objectName = sqlobject['name'] ,
                                           filename = sqlobject['filename'],
                                           dependentTableName= table,
                                           uuid = str(uuid.uuid1())
                                        )
                session.add(dbentry)
                session.commit()
        session.close()


    def bulkinsertdep(self):
        bulkinsertlimi = 100
        session = Session()
        bulkinsertobjects = list() 

        for sqlobject in self.dependencies:
            for table in sqlobject['tables']:
                dbentry = TableDependency( objectName = sqlobject['name'] ,
                                           filename = sqlobject['filename'],
                                           dependentTableName= table,
                                           uuid = str(uuid.uuid1())
                                        )
                bulkinsertobjects.append(dbentry)
        
        session.bulk_save_objects(bulkinsertobjects)
        session.commit()
        session.close()



    def start(self):
        #self.allfiles = self.findFiles()
        self.parseSql()
        self.insertdep()
        #self.bulkinsertdep()



if __name__ == "__main__":
    c = Runner()
    c.findFiles()
    #c.unitendtest()
    #c.parseCTE()
    print( c.start() )
    # print(c.parseSql() )



