from app.models import db_session
from flask import Flask

app = Flask(__name__)

#自动关闭db_session
@app.teardrown_request
def shutdown_session(exception = None):
    db_session.remove()