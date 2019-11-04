from main.sql_parser.snowsqlparser import ParseSql
from main.sql_parser.file_finder import FileFinder
from main.database.db_engine import Session
from main.database.models import TableDependency
import uuid
#import multiprocessing
from multiprocessing import Pool, cpu_count
import cProfile
import time


class Runner(object):
    def __init__(self):
        self.allfiles = None
        self.dependencies = list()
        self.proccess = self.determine_max_proc()

    def findFiles(self):
        self.allfiles = FileFinder().getListOfFiles()
    
    def parseSql(self):
        for file in self.allfiles:
            self.dependencies.append(ParseSql(file=file).getfinalFrom())
    
    def exp_para_parseSql(self, file):
        self.dependencies.append(ParseSql(file=file).getfinalFrom())

    def para_parseSql(self):
        number_of_processcess = self.determine_max_proc() - 1
        print(f"starting with number of processes: {number_of_processcess} ")
        p = Pool(number_of_processcess)
        p.map(self.exp_para_parseSql, self.allfiles )
    
    def determine_max_proc(self):
        return cpu_count()

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
        #self.para_parseSql()
        #self.insertdep()
        self.bulkinsertdep()



if __name__ == "__main__":
    starttime = time.time()
    c = Runner()
    c.findFiles()
    #c.unitendtest()
    #c.parseCTE()
    print( c.start() )
    endtime = time.time()
    print('Time needed:', endtime - starttime )
    # print(c.parseSql() )
    





