from flask import Blueprint, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user
from app.models.models import User

bp = Blueprint("session", __name__, url_prefix="/session")

@bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        print("here")
        # TODO determine and implement what to do on a successful authentication
        pass
    # TODO get the data from the request to verify if valid to login
    if request.method == "POST":
        data = request.get_json()
        print(data)
        email = data.email
        password = data.password
        user = User.query.filter(user.email == email).first()
        if not User or not User.check_password(password):
            return redirect(url_for(".login"))
        login_user(User)
    return jsonify({"todo":"needs work"})


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for(".login"))
