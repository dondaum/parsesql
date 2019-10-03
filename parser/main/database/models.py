from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class TableDependency(Base):
    __tablename__ = 'tabledependencies'
    # dep_id_seq = Sequence('dep_id_seq')
    #id = Column(Integer, dep_id_seq , primary_key=True)
    uuid = Column(String, primary_key=True)
    filename            = Column(String)
    objectName          = Column(String)
    dependentTableName  = Column(String)
