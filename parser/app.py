from main.sql_parser.snowsqlparser import ParseSql
from main.sql_parser.file_finder import FileFinder
from main.database.db_engine import Session
from main.database.models import TableDependency
import uuid
#import multiprocessing
from multiprocessing import Pool, cpu_count, Queue
import cProfile
import time


class Runner(object):
    def __init__(self, parallelism=1):
        self.allfiles = None
        self.dependencies = list()
        self.parallelism = parallelism
        self.proccess = self.determine_max_proc()
        self.executer = self.get_executer()

    def get_executer(self):
        if self.parallelism <= 0:
            return SequentialExecuter()
        else:
            return MultiProcessingExecuter()

    def dryrun(self):
        self.executer.to_parse_files = self.allfiles
        result = self.executer.run()
        self.dependencies = result
     
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
        # p = Pool(number_of_processcess)
        # p.map(self.exp_para_parseSql, self.allfiles )

        with Pool(processes=number_of_processcess) as pool:
            data = pool.map(self.exp_para_parseSql, self.allfiles)
            self.dependencies = data
            print('-------------------')
            print(f'Typ {type(data)}')
            print(data)
    
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
        self.dryrun()
        #self.parseSql()
        #self.para_parseSql()
        #self.insertdep()
        self.bulkinsertdep()

class BaseExecuter(object):
    pass

class SequentialExecuter(BaseExecuter):
    pass

class MultiProcessingExecuter(BaseExecuter):

    def __init__(self, to_parse_files=None):
        self.to_parse_files = to_parse_files

    def determine_max_proc(self):
        return cpu_count()

    def parse(self, file):
        return ParseSql(file=file).getfinalFrom()

    def run(self):
        number_of_processcess = self.determine_max_proc() - 1

        p = Pool(number_of_processcess)
        return p.map( self.parse , self.to_parse_files )

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
    





