from app.models import engine
from app.models import dbmetadata
from app.models import db_session
from app.models.role_model import Role 
from app.models.user_model import User
from app.models.comment_model import Comment
from app.models.post_model import Post
from app.models.follow_model import Follow 

#SQL 实例化


def init_db():
    # import models
    dbmetadata.create_all(bind=engine)









                                        

