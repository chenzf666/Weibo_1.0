from . import Base
from . import db_session
from flask import current_app
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from .Permissions import Permission 
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from .role_model import Role 
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash


class User(Base,UserMixin):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique = True)
    email = Column(String(120),unique = True)
    password_hash = Column(String(128),nullable = False)
    location = Column(String(64))
    about_me = Column(Text)
    member_since = Column(DateTime,default = datetime.utcnow)
    last_seen = Column(DateTime,default = datetime.utcnow)
    avatar_hash = Column(String(32))

    #foreignkey 
    role_id = Column(Integer, ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %s %s %s>' %(self.name,self.email,self.role)

    #初始化 赋予默认角色
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter(Role.permissions == 0xff).first()
            if self.role is None:
                self.role = Role.query.filter(Role.default == True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()       


    #最后一次时间 更新, 或许可以放置service 层实现
    def ping(self):
        self.last_seen = datetime.utcnow()
        db_session.add(self)
        db.session.commit()                

    #权限检测，或许可以放置service 层实现
    def can(self,permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)        

    #密码属性字段，密码哈希生成，以及密码验证
    @property
    def password(self):
        pass

    @password.setter
    def password(self,password):
        self.password_hash =  generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #to_json    
    def to_json(self):
        json_user = {
            #'url':url_for('..',id = self.id,_external = True),
            'name':self.name,
            'email':self.email,
            'location':self.location,
            'about_me':self.about_me,
            'member_since':self.member_since,
            'last_seen':self.last_seen
        }
        return json_user        


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False 




