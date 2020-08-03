from flask import Blueprint, url_for, render_template, redirect
from app.models import db, Location
from app.forms import Form

bp = Blueprint("location", __name__, url_prefix="/location")

@bp.route("/", methods=["GET"])
def get_all_locations():
    locations = Location.query.all()
    return render_template("location.html", locations=locations)

@bp.route("/", methods=["GET"])
def get_location(location_id):
    location = Location.query.filter_by(location_id).all()
    return render_template('location.html', location=location)

@bp.route("/", methods=["POST"])
def create_location():
    # obtain form data for location
    form = Form()
    if form.validate_on_submit():
        data = form.data # obtain data from the form
        # construct of location with form data
        location = Location(data.address, data.city, data.state, data.gps_coords, data.images, data.website, data.description, data.host_notes, data.active)
        # add and commit to the database
        db.session.add(location)
        db.session.commit()
    else:
        return '<h1>Bad Data</h1>'

@bp.route("/", methods=["PUT"])
# Update a location with new data
