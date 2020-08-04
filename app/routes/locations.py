from flask import Blueprint, url_for, redirect, request, jsonify
from app.models import db, Location, Amenities, Necessities

bp = Blueprint("location", __name__, url_prefix="/location")

@bp.route("/", methods=["GET"])
def get_all_locations():
    locations = Location.query.all()
    return jsonify(locations)

@bp.route("/", methods=["GET"])
def get_location(location_id):
    # get location by location_id
    location = Location.query.filter_by(location_id).one()
    return jsonify(location)

@bp.route("/", methods=["POST"])
def create_location():
    # obtain form data for location
    if request:
        data = request # obtain data from the form
        # construct of location with form data
        location = Location(data.address, data.city, data.state, data.gps_coords, data.images, data.website, data.description, data.host_notes, data.active)
        amenities = Amenities(data.electric_hookup, data.water_hookup, data.septic_hookup, data.assigned_parking, data.tow_vehicle_parking, data.trash_removal, data.water_front, data.pets_allowed, data.internet_access)
        necessities = Necessities(data.rv_compatible, data.generators_allowed, data.fires_allowed, data.max_days, data.pet_type)
        # add and commit to the database
        db.session.add(location)
        db.session.add(amenities)
        db.session.add(necessities)
        db.session.commit()
    else:
        return jsonify("Bad Data")

@bp.route("/", methods=["PUT"])
# Update a location with new data
