from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///parsersql.db', echo=True)
Session = sessionmaker(bind=engine)






