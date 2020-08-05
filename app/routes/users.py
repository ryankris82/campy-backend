from flask import Blueprint, render_template, jsonify, request
from app.models.models import db, User
from flask_jwt_extended import  jwt_required

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/<user_id>", methods=["GET"])
@jwt_required
def get_one_user(user_id):
    user = User.query.get(int(user_id))
    if user == None:
        return jsonify({"message": "no user found for the requested id"})

    return jsonify({"user":user.to_dictionary()})

@bp.route("/<user_id>", methods=["PUT"])
@jwt_required
def update_user(user_id):
    user = User.query.get(int(user_id))
    if user == None:
        return jsonify({"message": "no user found for the requested id"})
    if request.is_json:
        image = request.json["image"]
        password = request.json["password"]
        phone_number = request.json["phoneNumber"]
        user_Info = request.json["userInfo"]
        domicile_type = request.json["domicileType"]
        first_name = request.json["firstName"]
        last_name = request.json["lastName"]
    else:
        image = request.form["image"]
        password = request.form["password"]
        phone_number = request.form["phoneNumber"]
        user_Info = request.form["userInfo"]
        domicile_type = request.form["domicileType"]
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]

    user.image = image
    user.password = password
    user.phone_number = phone_number
    user.user_Info= user_Info
    user.domicile_type = domicile_type
    user.first_name = first_name
    user.last_name = last_name
    db.session.commit()

    return jsonify(message="User record updated successfully.")
