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

@bp.route("/<user_id>", methods=["PUT"])
def update_user():
    # TODO
    return jsonify({"message":"update user"})
