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

from multiprocessing import Pool, cpu_count
from parsesql.main.sql_parser.snowsqlparser import ParseSql


class BaseExecuter(object):
    pass


class SequentialExecuter(BaseExecuter):

    def __init__(self, to_parse_files=None):
        self.to_parse_files = to_parse_files

    def parse(self):
        dependencies = list()
        for file in self.to_parse_files:
            dependencies.append(ParseSql(file=file).parse_dependencies())
        return dependencies

    def run(self):
        return self.parse()


class MultiProcessingExecuter(BaseExecuter):

    def __init__(self, to_parse_files=None):
        self.to_parse_files = to_parse_files

    def determine_max_proc(self):
        return cpu_count()

    def parse(self, file):
        return ParseSql(file=file).parse_dependencies()

    def run(self):
        number_of_processcess = self.determine_max_proc() - 1

        p = Pool(number_of_processcess)
        return p.map(self.parse, self.to_parse_files)
