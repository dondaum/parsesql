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

engine = create_engine('sqlite:///{0}'.format(sqlite_db_file))

connection = engine.connect()

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

