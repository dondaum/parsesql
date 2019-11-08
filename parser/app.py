from main.sql_parser.snowsqlparser import ParseSql
from main.sql_parser.file_finder import FileFinder
from main.database.db_engine import Session
from main.database.models import TableDependency
from main.executers import SequentialExecuter, MultiProcessingExecuter
import uuid
import cProfile
import time


class Runner(object):
    def __init__(self, parallelism=0):
        self.allfiles = None
        self.dependencies = list()
        self.parallelism = parallelism
        self.executer = self.get_executer()

    def get_executer(self):
        if self.parallelism <= 0:
            return SequentialExecuter()
        else:
            return MultiProcessingExecuter()

    def parseSql(self):
        self.executer.to_parse_files = self.allfiles
        result = self.executer.run()
        self.dependencies = result
     
    def findFiles(self):    
        self.allfiles = FileFinder().getListOfFiles()

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

        if not self.dependencies:
            print('There are no table dependencies.')

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
        self.findFiles()

        #self.allfiles = self.findFiles()

        self.parseSql()
        #self.para_parseSql()
        #self.insertdep()
        #self.bulkinsertdep()


if __name__ == "__main__":
    starttime = time.time()
    c = Runner()
    c.start()
    #c.findFiles()
    #c.unitendtest()
    #c.parseCTE()
    
    #print( c.start() )
    endtime = time.time()
    print('Time needed:', endtime - starttime )
    
    # print(c.parseSql() )
    





