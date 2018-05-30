from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from . import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    body = Column(Text)
    title = Column(String(64))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    body_html = Column(Text)

    # foreignkey
    author_id = Column(Integer, ForeignKey("users.id"))

    # relationship
    comments = relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return "<Post %s %s %s>" % (self.id, self.title, self.timestamp)

    def to_json(self):
        json_post = {
            # "url":,
            # "author":url_for(),
            "body": self.body,
            "title": self.title,
            "timestamp": self.timestamp,
            "body_html": self.body_html,
        }
        return json_post
