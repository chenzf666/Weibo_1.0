from . import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique = True)
    email = Column(String(120),unique = True)
    password = Column(String(64),nullable = False)

    #foreignkey 
    role_id = Column(Integer, ForeignKey('roles.id'))
    