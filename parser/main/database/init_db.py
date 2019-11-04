from db_engine import Session, db_engine
from models import TableDependency, Base

Base.metadata.drop_all(db_engine)
# 1 - generate database schema
Base.metadata.create_all(db_engine)

# 2 - check connection
session = Session()
session.commit()
session.close()