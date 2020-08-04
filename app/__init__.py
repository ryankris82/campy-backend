from flask import Flask
from app.config import Configuration
from flask_login import LoginManager
from app.models.models import db, User
from app.routes import session, users
from flask_migrate import Migrate


app = Flask(__name__)


app.config.from_object(Configuration)
db.init_app(app)

Migrate(app, db)
# run only the last command
# pipenv run flask db init
# pipenv run flask db migrate -m 'first migration'
# pipenv run flask db upgrade

# TODO add routes here
app.register_blueprint(users.bp)
app.register_blueprint(session.bp)

login = LoginManager(app)
login.login_view = "session.login"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return 'hello'
