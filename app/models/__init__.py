from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker



engine = create_engine(...)#sql url
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,
                                        bind=engine)

dbmetadata = MetaData()
Base = declarative_base(metadata = dbmetadata)
Base.query = db_session.query_property()

