from flask import Flask
from .config import Configuration
from flask_login import LoginManager
from models.User import db, User

app = Flask(__name__)
app.config.from_object(Configuration)

# TODO add routes here

login = LoginManager(app)
login.login_view = "session.login"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
