from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
from config.config_reader import Config

class DatabaseEngine():
        def __init__(self, strategy='sqllite'):
                self.strategy = strategy

        def get_engine(self):
                if self.strategy == 'sqllite':
                        return self.get_engine_sqllite()
                if self.strategy == 'snowflake':
                        return self.get_snowflake_engine()
        
        def get_engine_sqllite(self):
                return create_engine('sqlite:///parsersql.db', echo=True)
        
        def get_snowflake_engine(self):
                return create_engine(URL(
                                user=Config.snowflake_account['user'],
                                password= Config.snowflake_account['password'],
                                account=Config.snowflake_account['account'],
                                database=Config.snowflake_account['database'],
                                schema = Config.snowflake_account['schema']
                        )
                        , echo=True

                        )
db_engine = DatabaseEngine(strategy='snowflake').get_engine()
Session = sessionmaker(bind=db_engine)






