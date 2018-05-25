from . import Base
from flask import current_app
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from .Permissions import Permission 
from flask_login import UserMixin
from flask_login import AnonymousUserMixin

from werkzeug.security import generate_password_hash


class User(Base,UserMixin):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique = True)
    email = Column(String(120),unique = True)
    password_hash = Column(String(128),nullable = False)

    #foreignkey 
    role_id = Column(Integer, ForeignKey('roles.id'))

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter(permissions == 0xff).first()
            if self.role is None:
                slef.role = Role.query.filter(default = True).first()    

    #权限检测
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
            'email':self.email
        }
        return json_user        


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False 




