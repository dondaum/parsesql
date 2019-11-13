from multiprocessing import Pool, cpu_count, Queue
from main.sql_parser.snowsqlparser import ParseSql

class BaseExecuter(object):
    pass

class SequentialExecuter(BaseExecuter):
    
    def __init__(self, to_parse_files=None):
        self.to_parse_files = to_parse_files

    def parse(self):
        dependencies = list()
        for file in self.to_parse_files:
            dependencies.append(ParseSql(file=file).getfinalFrom())
        return dependencies

    def run(self):
        return self.parse()

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