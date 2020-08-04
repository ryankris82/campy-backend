
from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("users", __name__, url_prefix="")

@bp.route("/")
@login_required
def index():
    # TODO get user
    return users
