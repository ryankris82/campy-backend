from flask import Blueprint, url_for, redirect, request, jsonify
from app.models.models import db, Location, Amenity, Necessity
from flask_jwt_extended import  jwt_required
from flask_restx import Resource, Namespace, fields

api = Namespace('/locations', description='Locations related operations')


# @api.route("/", methods=["GET"])
# class Location(Re)
# def get_all_locations():
#     locations = Location.query.all()
#     data = [location.to_dictionary() for location in locations]
#     return {"locations":data}

# @bp.route("/", methods=["GET"])
# def get_location(location_id):
#     # get location by location_id
#     location = Location.query.filter_by(location_id).one()
#     return jsonify(location)

# @bp.route("/", methods=["POST"])
# def create_location():
#     # obtain request data for location
#     if request:
#         data = request # obtain data from the form
#         # construct of location with form data
#         location = Location(data.address, data.city, data.state, data.gps_coords, data.images, data.website, data.description, data.host_notes, data.active)
#         amenities = Amenity(data.electric_hookup, data.water_hookup, data.septic_hookup, data.assigned_parking, data.tow_vehicle_parking, data.trash_removal, data.water_front, data.pets_allowed, data.internet_access)
#         necessities = Necessity(data.rv_compatible, data.generators_allowed, data.fires_allowed, data.max_days, data.pet_type)
#         # add and commit to the database
#         db.session.add(location)
#         db.session.add(amenities)
#         db.session.add(necessities)
#         db.session.commit()
#     else:
#         return jsonify("Bad Data")

# @bp.route("/<int:location_id>", methods=["PUT"])
# # Update a location with new data
# def edit_location(location_id):
#     # Get the location to edit by id
#     if request.id == location_id:
#         data = request
#         # Get the location to update by its id
#         updateLoc = Location.query.filter_by(id=location_id).first()
#         # Get the amenities by the location's foreign key for amenities
#         updateAmen = Amenities.query.filter_by(id=updateLoc.amenities_id).first()
#         # Get the amenities by the location's foreign key for necessities
#         updateNeci = Necessities.query.filter_by(id=updateLoc.necessities_id).first()

#         # update the retrieved rows in these tables (location, amenities, and necessities) with the request data
#         updateLoc = {
#             'address': data.address,
#             'city': data.city,
#             'state': data.state,
#             'gps_coords': data.gps_coords,
#             'images': data.images,
#             'website': data.website,
#             'description': data.description,
#             'host_notes': data.host_notes,
#             'active': data.active,
#         }

#         updateAmen = {
#             'electric_hookup': data.electric_hookup,
#             'water_hookup': data.water_hookup,
#             'septic_hookup': data.septic_hookup,
#             'assigned_parking': data.assigned_parking,
#             'tow_vehicle_parking': data.tow_vehicle_parking,
#             'trash_removal': data.trash_removal,
#             'water_front': data.water_front,
#             'pets_allowed': data.pets_allowed,
#             'internet_access': data.internet_access,
#         }

#         updateNeci = {
#             'rv_compatible': data.electric_hookup,
#             'generators_allowed': data.generators_allowed,
#             'fires_allowed': data.fires_allowed,
#             'max_days': data.max_days,
#             'pad_type': data.pad_type,
#         }

#         # commit the above changes to the database
#         db.session.commit()

# @bp.route("/<int:location_id", methods=['DELETE'])
# # Delete a location and it's dependent Amenities and Necessities rows.
# def delete_location_by_id(location_id):
#     if request.id == location_id:
#         # obtain the 3 rows of data in these 3 rel. tables (location, amenities, and necessities)
#         location_to_del = Location.query.filter_by(location_id).first()
#         amenities_to_del = Amenities.query.filter_by(location_to_del.amenities_id).first()
#         necessities_to_del = Necessities.query.filter_by(location_to_del.necessities_id).first()

#         # look into way to DRY up these 3 lines
#         db.session.delete(necessities_to_del)
#         db.session.delete(amenities_to_del)
#         db.session.delete(location_to_del)

#         db.session.commit()
