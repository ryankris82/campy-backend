from flask import Flask
from app.config import Configuration
from app.models.models import db, User
from app.routes import users, auth, locations
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.routes.auth import bp as api

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

jwt = JWTManager(app)
app.config.from_object(Configuration)
db.init_app(app)

Migrate(app, db)
# run only the last command
# pipenv run flask db init
# pipenv run flask db migrate -m 'first migration'
# pipenv run flask db upgrade

# TODO add routes here
# app.register_blueprint(users.bp)
app.register_blueprint(api)
# app.register_blueprint(locations.bp)
