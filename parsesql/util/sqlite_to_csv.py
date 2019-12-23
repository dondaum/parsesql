# MIT License

# Copyright (c) 2019 Sebastian Daum

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, csv
from sqlalchemy import create_engine, exc, MetaData, Table
from sqlalchemy.sql import select

base = os.path.dirname(os.path.abspath(__file__))
base_parent = os.path.dirname(base)
sqlite_db_file = os.path.join(base_parent, 'parsersql.db')
outcsv = 'dev_viewdefinitions.csv'  # for now, not configurable
failedcsv = 'dev_viewdefinitions_failed.csv'
# helper functions
def split_row(rowproxy):
    splittable=True
    row=[]
    row_as_list=[]
    for column, value in rowproxy.items():
        row_as_list.append(value)

    try:
        row = [row_as_list[2].split('.')[0], row_as_list[2].split('.')[1], row_as_list[3].split('.')[0], row_as_list[3].split('.')[1]]
        #row = [v.strip(" \"'[]") for v in split_row]
    except IndexError:
        row=row_as_list
        splittable=False
    except AttributeError:
        row=row_as_list
        splittable=False
    return row, splittable
#TODO: Check if this path works system independent
engine = create_engine('sqlite:///{0}'.format(sqlite_db_file))

connection = engine.connect()

#TODO: This should be included from the existing sqlalchemy metdata
metadata = MetaData()
tabledependencies = Table('tabledependencies', metadata, autoload=True, autoload_with=engine)

select_stmt=select([tabledependencies])
resultlist = []
failedlist = []
try:
    # suppose the database has been restarted.
    result = connection.execute(select_stmt)
    for rowproxy in result:
        row, splittable = split_row(rowproxy)
        if splittable:
            resultlist.append(row)
        else:
            failedlist.append(row)
    connection.close()
except exc.DBAPIError as e:
     # an exception is raised, Connection is invalidated.
     if e.connection_invalidated:
         print("Connection was invalidated!")

with open(outcsv, 'w') as outfile:
    outwriter = csv.writer(outfile)
    outwriter.writerows(resultlist)

with open(failedcsv, 'w') as failedfile:
    outwriter = csv.writer(failedfile)
    outwriter.writerows(failedlist)

