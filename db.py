from app.models import engine
from app.models import dbmetadata
from app.models import db_session
from app.models.role_model import Role
from app.models.user_model import User
from app.models.comment_model import Comment
from app.models.post_model import Post
from app.models.follow_model import Follow
from app.models.classification_model import Classification
#SQL 实例化
from app.models import engine
from app.models import db_metadata
from app.models import db_session
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(bind=engine)
session = DBSession()




#SQL 实例化


from app.repositories.base_repository import SQLAlchemyRepository
UserSQL=SQLAlchemyRepository(User,session)
RoleSQL=SQLAlchemyRepository(Role,session)
CommentSQL=SQLAlchemyRepository(Comment,session)
ClassificationSQL=SQLAlchemyRepository(Classification,session)
FollowSQL=SQLAlchemyRepository(Follow,session)

def init_db():
    # import models
    db_metadata.create_all(bind=engine)
















