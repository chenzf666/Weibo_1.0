from .models import db_session
from flask import Flask
from .models.user_model import User
from .models.user_model import AnonymousUser
from flask_login import LoginManager
#from .models import init_db
from db import init_db
from config import Config


webapp = Flask(__name__)

login_manager = LoginManager()
login_manager.session_protection ='Strong'
#login_manager.login_view = ''
login_manager.init_app(webapp)
login_manager.anonymous_user = AnonymousUser


init_db()
webapp.config.from_object(Config)



#自动关闭db_session
@webapp.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    