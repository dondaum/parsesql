from db_engine import Session, enginesqllite, enginesnow
from models import TableDependency, Base

Base.metadata.drop_all(enginesqllite)
# 1 - generate database schema
Base.metadata.create_all(enginesqllite)

# 2 - check connection
session = Session()
session.commit()
session.close()