from flask import Blueprint, redirect, url_for, request, jsonify
from app.models.models import User
from flask_jwt_extended import  jwt_required, create_access_token


bp = Blueprint("auth", __name__, url_prefix="/")

@bp.route("/signup", methods=["POST"])
def signup():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify( message = "The email already exists."), 409
    else:
        password = request.form["password"]
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        domicile_type = request.form["domicileType"]
        phoneNumber = request.form["phoneNumber"]
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            domicile_type=domicile_type,
            phone_number=phoneNumber
            )
        print("user====>", user)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="successfully created user."), 201


@bp.route("/login", methods=["POST"] )
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    user = User.query.filter_by(email=email).first()
    print(user)
    if  user:
        valid= user.check_password(password)
        if valid:
            access_token = create_access_token(identity=email)
            return jsonify( message = "Login successful!", access_token=access_token)
    else:
        return jsonify( message = "Bad email or password."), 401
