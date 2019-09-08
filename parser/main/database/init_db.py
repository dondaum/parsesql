from db_engine import Session, engine
from models import TableDependency, Base

# 1 - generate database schema
Base.metadata.create_all(engine)

# 2 - check connection
session = Session()
session.commit()
session.close()