from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    domicile_type = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    user_info = db.Column(db.String(2000))
    createdAt = db.Column(db.DateTime)
    updateddAt = db.Column(db.DateTime)
    hashed_password = db.Column(db.String(100), nullable=False)
