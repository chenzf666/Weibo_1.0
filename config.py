# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 密钥，保护所有表单免受跨站请求伪造（CSRF）的攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JSON_AS_ASCII = False
    # 邮件主题的前缀
    FLASKY_MAIL_SUBJECT_PREFIX = None
    # 发件人的地址
    FLASKY_MAIL_SENDER = '1660823093@qq.com'
    # 电子邮件的收件人
    FLASKY_ADMIN = '1660823093@qq.com'
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    STATIC_PATH = 'app'
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '1660823093@qq.com'
    MAIL_PASSWORD = 'unahpciblvsgcgad'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:22621821@127.0.0.1:3306/mydatabase?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:22621821@127.0.0.1:3306/mydatabase?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:22621821@127.0.0.1:3306/mydatabase?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
