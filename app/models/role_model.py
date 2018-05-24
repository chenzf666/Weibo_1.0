from . import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from . import db_session


class Permission:
    FOLLOW = 0x01
    COMMIT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS =0x08
     

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique=True)
    permission = Column(Integer)

    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return '<Role %s>' %(self.name)

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW | \
                Permission.COMMIT | \
                Permission.WRITE_ARTICLES,True),

            'Moderator':(Permission.FOLLOW | \
                Permission.COMMIT | \
                Permission.WRITE_ARTICLES | \
                MODERATE_COMMENTS,True),

            'Administrator':(0xff,False)
        }

        for r in roles:
            role = Role.query.filter(name == r).first()
            if role is None:
                  role = Role(name = r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db_session.add(role)
        db_session.commit(role)      