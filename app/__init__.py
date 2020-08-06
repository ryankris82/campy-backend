from flask import Flask
from app.config import Configuration
from app.models.models import db, User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.routes.auth import api as auth
from app.routes.locations import api as locations
from app.routes.users import api as users

app = Flask(__name__)

jwt = JWTManager(app)
app.config.from_object(Configuration)
db.init_app(app)

api = Api(app)
api.add_namespace(auth)
api.add_namespace(locations)
api.add_namespace(users)


Migrate(app, db)
# run only the last command
# pipenv run flask db init
# pipenv run flask db migrate -m 'first migration'
# pipenv run flask db upgrade
