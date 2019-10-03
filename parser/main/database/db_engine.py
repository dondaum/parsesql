from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
import sys
sys.path.append('C:\\Users\\s40844\\Documents\\python_connector')
import secret as se

enginesqllite = create_engine('sqlite:///parsersql.db', echo=True)


enginesnow =  create_engine(URL(
                user=se.credential['user'],
                password=se.credential['password'],
                account='eonenergiedeutschland.eu-central-1',
                database='SALESBI_DB_PROD',
                schema = se.credential['schema']
        )
        , echo=True
        )

Session = sessionmaker(bind=enginesqllite)






