import hashlib
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from . import Base
from .role_model import Role


#  PEP8:
#  一般import package放第一层
#  from package import fun第二层
#  自己的包为第三层

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    password_hash = Column(String(128), nullable=False)
    location = Column(String(64))
    about_me = Column(Text)
    member_since = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    avatar_hash = Column(String(32))

    # foreignkey
    role_id = Column(Integer, ForeignKey('roles.id'))
    posts = relationship('Post', backref='author', lazy='dynamic')
    followed = relationship('Follow', back_populates="follower")
    follower = relationship('Follow', back_populates="followed")
    comments = relationship('Comment', backref='author', lazy='dynamic')

    # 初始化 赋予默认角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter(Role.permissions == 0xff).first()
            if self.role is None:
                self.role = Role.query.filter(Role.default == True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User {} {} {} {}>'.format(self.id, self.name, self.email, self.role)
        #  .format()是py3  %()是继承py2的

    def to_json(self):
        json_user = {
            # 'url':url_for('..',id = self.id,_external = True),
            'name': self.name,
            'email': self.email,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since,
            'last_seen': self.last_seen
        }
        return json_user

    '''
    service layer:
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db_session.add(self)
        db_session.commit()

        #  权限检测，或许可以放置service 层实现

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

        #  密码属性字段，密码哈希生成，以及密码验证

    #  我打算在service层弄个验证密码和修改密码的接口替换这个
    @property
    def password(self):
        pass

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    '''
