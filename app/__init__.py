from flask import Flask
from app.config import Configuration
from app.models.models import db, User
from app.routes import users, auth
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

jwt = JWTManager(app)
app.config.from_object(Configuration)
db.init_app(app)


Migrate(app, db)
# run only the last command
# pipenv run flask db init
# pipenv run flask db migrate -m 'first migration'
# pipenv run flask db upgrade

# TODO add routes here
app.register_blueprint(users.bp)
app.register_blueprint(auth.bp)

@app.route('/')
def index():
    return 'hello'
