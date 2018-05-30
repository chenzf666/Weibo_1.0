from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from . import Base


class Follow(Base):
    __tablename__ = "follows"
    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # relationship
    user_follower = relationship('User', back_populates="followed")
    user_followed = relationship('User', back_populates="follower")

    def to_json(self):
        pass