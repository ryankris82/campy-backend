from flask import Blueprint, render_template, jsonify, request
from app.models.models import db, User
# from flask_login import login_required

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/<user_id>", methods=["GET"])
# @login_required
def get_one_user(user_id):
    user = User.query.get(int(user_id))
    if user == None:
        return jsonify({"message": "no user found for the requested id"})

    return jsonify({"user":user.to_dictionary()})

@bp.route("/", methods=["POST"])
def create_user():
    if request.method == "POST":
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        first_name = data["firstName"]
        last_name = data["lastName"]
        domicile_type = data["domicileType"]
        phoneNumber = data["phoneNumber"]
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
    return jsonify({"message":"successfully created user"})

@bp.route("/<user_id>", methods=["PUT"])
def update_user():
    # TODO
    return jsonify({"message":"update user"})
