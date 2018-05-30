from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from . import Base
from . import db_session


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    body = Column(Text)
    body_html = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    disabled = Column(Boolean)

    # foreignkey
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def to_json(self):
        json_comment = {
            "body": self.body,
            "body_html": self.body_html,
            "timestamp": self.timestamp,
            "disabled": self.disabled
        }
        return json_comment
