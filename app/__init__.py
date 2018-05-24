from app.models import db_session
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.session_protection ='Strong'
#login_manager.login_view = ''
login_manager.init(app)

#自动关闭db_session
@app.teardrown_request
def shutdown_session(exception = None):
    db_session.remove()