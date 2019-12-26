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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
from parsesql.config.config_reader import Config
from sqlalchemy import create_engine

class DatabaseEngine():
        def __init__(self):
                self.strategy = Config.strategy

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
                                schema = Config.snowflake_account['schema'],
                                warehouse = Config.snowflake_account['warehouse']
                                )
                        , echo=True
                )

db_engine = DatabaseEngine().get_engine()
Session = sessionmaker(bind=db_engine)






