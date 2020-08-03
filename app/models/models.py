from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    domicile_type = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    user_info = db.Column(db.String(2000))
    createdAt = db.Column(db.)
    updateddAt = db.Column(db.)
    hashed_password = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
