# MIT License

# Copyright (c) 2019 Sebastian Daum

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from parsesql.main.sql_parser.file_finder import FileFinder
from parsesql.main.database.db_engine import Session
from parsesql.main.database.models import TableDependency
from parsesql.main.sql_parser.snowsqlparser import ParseSql
from parsesql.main.executers import SequentialExecuter, MultiProcessingExecuter
import uuid
import time


class Runner():
    """
    :param bulk_load: if true all insert will hapen in a bulk load else single
    INSERTs in the database
    :param parallelism: if > 0 then work gets applied on multiple cpus. Notice
    this will reduce work on number of cpus on machine minus - 1. So if your
    machine has 4 cpus it will run on max 3 cpus concurrently even if 8 is
    given as a parameter
    """
    def __init__(self, parallelism=0, bulk_load=True):
        self.allfiles = None
        self.dependencies = []
        self.parallelism = parallelism
        self.bulk_load = bulk_load
        self.executer = self._get_executer()

    def _get_executer(self):
        """
        factory class method that return correct executer
        """
        if self.parallelism <= 0:
            return SequentialExecuter()
        else:
            return MultiProcessingExecuter(cpu_cores=self.parallelism)

    def start_sql_parsing(self) -> None:
        """
        main sql parsing method that searches for files, prime and config
        executer and call run method
        """
        self.search_files()
        self.executer.target_list = self.allfiles
        self.executer.klass = ParseSql
        self.executer.klass_method_name = "parse_dependencies"
        self.dependencies = self.executer.run()

    def search_files(self) -> None:
        """
        Instance method that searches all files
        """
        self.allfiles = FileFinder().getListOfFiles()

    def _data_load(self):
        """
        factory method that either single or bulk insert data in the
        database
        """
        if self.bulk_load:
            self._bulkinsertdep()
        else:
            self._insertdep()

    def _insertdep(self) -> None:
        session = Session()
        for sqlobject in self.dependencies:
            for table in sqlobject['tables']:
                dbentry = TableDependency(objectName=sqlobject['name'],
                                          filename=sqlobject['filename'],
                                          dependentTableName=table,
                                          uuid=str(uuid.uuid1())
                                          )
                session.add(dbentry)
                session.commit()
        session.close()

    def _bulkinsertdep(self) -> None:
        session = Session()
        bulkinsertobjects = list()
        for sqlobject in self.dependencies:
            for table in sqlobject['tables']:
                dbentry = TableDependency(objectName=sqlobject['name'],
                                          filename=sqlobject['filename'],
                                          dependentTableName=table,
                                          uuid=str(uuid.uuid1())
                                          )
                bulkinsertobjects.append(dbentry)
        session.bulk_save_objects(bulkinsertobjects)
        session.commit()
        session.close()

    def start(self) -> None:
        self.start_sql_parsing()
        self._data_load()


if __name__ == "__main__":
    starttime = time.time()
    Runner(parallelism=8, bulk_load=True).start()
    endtime = time.time()
    print('Time needed:', endtime - starttime)
