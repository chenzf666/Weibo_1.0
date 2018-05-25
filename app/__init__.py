from .models import db_session
from flask import Flask
from .models.user_model import User
from flask_login import LoginManager
#from .models import init_db
from db import init_db


webapp = Flask(__name__)

login_manager = LoginManager()
login_manager.session_protection ='Strong'
#login_manager.login_view = ''
login_manager.init_app(webapp)
init_db()



#自动关闭db_session
@webapp.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    