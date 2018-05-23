from app.models import engine
from app.models import db_metadata
from app.models import db_session

#SQL 实例化


def init_db():
    # import models
    db_metadata.create_all(bind=engine)









                                        

