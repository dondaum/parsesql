from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class TableDependency(Base):
    __tablename__ = 'tabledependencies'

    id = Column(Integer, primary_key=True)
    filename            = Column(String)
    objectName          = Column(String)
    dependentTableName  = Column(String)
