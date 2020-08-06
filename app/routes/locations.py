from app.models.models import db, Location, Amenity, Necessity, User
from flask_restx import Resource, Namespace, fields

api = Namespace('locations', description='Locations related operations')

model = api.model("Location",
                        {
                        "address": fields.String(required=True, description="Location address."),
                        "city": fields.String(required=True, description="Location city."),
                        "state": fields.String(required=True, description="Location state."),
                        "gps_coords": fields.String(required=True, description="Location GPS Coordinates."),
                        "image_urls": fields.List(fields.String( description="Location image URLs.")),
                        "website": fields.String( description="Location website."),
                        "description": fields.String(required=True, description="Location Description."),
                        "host_notes": fields.String( description="Location Host notes."),
                        "active": fields.Boolean( description="Location active."),
                        "user_id": fields.Integer(required=True, description="Location Host User Id."),

                        "electric_hookup":  fields.Boolean(required=True, description="Does location have electric hookup?"),
                        "water_hookup":  fields.Boolean(required=True, description="Does location have water hookup?"),
                        "septic_hookup":  fields.Boolean(required=True, description="Does location have septic hookup?"),
                        "assigned_parking":  fields.Boolean(required=True, description="Does location have an assigned parking?"),
                        "tow_vehicle_parking":  fields.Boolean(required=True, description="Does location have a tow vehicle parking?"),
                        "trash_removal":  fields.Boolean(required=True, description="Does location have trash removal?"),
                        "water_front":  fields.Boolean(required=True, description="Is location a water front?"),
                        "pets_allowed":  fields.Boolean(required=True, description="Does location allow pets?"),
                        "internet_access":  fields.Boolean(required=True, description="Does location have internet access?"),
                        "tow_vehicle_parking":  fields.Boolean(required=True, description="Does location have a tow vehicle parking?"),

                        "rv_compatible":  fields.Boolean(required=True, description="Is location  RV compatible."),
                        "generators_allowed":  fields.Boolean(required=True, description="Does location allow generators?"),
                        "fires_allowed":  fields.Boolean(required=True, description="Does location allow fires?"),
                        "max_days":  fields.Integer(required=True, description="Location's maximum stay days."),
                        "pad_type":  fields.String(required=True, description="Location's pad type."),
                        }
                )


@api.route("/")
class Locations(Resource):
    def get(self):
        '''Get all locations.'''
        locations = Location.query.all()
        data = [location.to_dictionary() for location in locations]
        return {"locations": data}

    @api.expect(model)
    def post(self):
        '''Create a new location to enjoy with the provided amenities, necessities data.'''
        data = api.payload

        amenity_data= {
            "electric_hookup":data["electric_hookup"],
            "water_hookup":data["water_hookup"],
            "septic_hookup":data["septic_hookup"],
            "assigned_parking":data["assigned_parking"],
            "tow_vehicle_parking":data["tow_vehicle_parking"],
            "trash_removal":data["trash_removal"],
            "pets_allowed":data["pets_allowed"],
            "internet_access":data["internet_access"]
        }

        # Check the database for the amenity record with the provided data
        # if a record is not found then create an Amenity record with the provided data
        amenity = Amenity.query.filter_by(
           electric_hookup = amenity_data["electric_hookup"],
           water_hookup = amenity_data["water_hookup"],
           septic_hookup = amenity_data["septic_hookup"],
           assigned_parking = amenity_data["assigned_parking"],
           tow_vehicle_parking = amenity_data["tow_vehicle_parking"],
           trash_removal = amenity_data["trash_removal"],
           pets_allowed = amenity_data["pets_allowed"],
           internet_access = amenity_data["internet_access"]).first() if None else Amenity(**amenity_data)

        data["amenity"]= amenity


        necessity_data = {
            "rv_compatible":data["rv_compatible"],
            "generators_allowed":data["generators_allowed"],
            "fires_allowed":data["fires_allowed"],
            "max_days":data["max_days"],
            "pad_type":data["pad_type"],
        }


        # Check the database for the amenity record with the provided data
        # if a record is not found then create an Amenity record with the provided data
        necessity = Necessity.query.filter_by(
            rv_compatible = necessity_data["rv_compatible"],
            generators_allowed = necessity_data["generators_allowed"],
            fires_allowed = necessity_data["fires_allowed"],
            max_days = necessity_data["max_days"],
            pad_type = necessity_data["pad_type"]).first() if None else Necessity(**necessity_data)

        data["necessity"]= necessity

        data["user"]=User.query.get(data["user_id"])

        # Clean up the data variable to contain only information needed to create
        #  the Location record using the ** operator (like a spread operation)
        data.pop("user_id")
        data.pop("electric_hookup")
        data.pop("water_hookup")
        data.pop("septic_hookup")
        data.pop("assigned_parking")
        data.pop("tow_vehicle_parking")
        data.pop("trash_removal")
        data.pop("water_front")
        data.pop("pets_allowed")
        data.pop("internet_access")

        data.pop("rv_compatible")
        data.pop("generators_allowed")
        data.pop("fires_allowed")
        data.pop("max_days")
        data.pop("pad_type")

        location = Location(**data)
        db.session.add(location)
        db.session.commit()

        return {"message": "Locations was successfully created!"}

@api.route("/<int:id>")
@api.response(404, 'Location not found')
class LocationById(Resource):
    def get(self, id):
        '''Get location information for the provided location id'''
        location = Location.query.get(int(id))
        if location:
            return {"location":location.to_dictionary()}
        else:
            return {"message": "Locations not found!"}, 404


    @api.expect(model)
    def put(self, id):
        '''Update location by location id using the data passed in'''
        location = Location.query.get(int(id))
        if location:
            data = api.payload

            location.address = data["address"]
            location.city = data["city"]
            location.state = data["state"]
            location.gps_coords = data["gps_coords"]
            location.image_urls = data["image_urls"]
            location.website = data["website"]
            location.description = data["description"]
            location.host_notes = data["host_notes"]
            location.active = data["active"]
            location.user = User.query.get(data["user_id"])

            amenity_data= {
                "electric_hookup":data["electric_hookup"],
                "water_hookup":data["water_hookup"],
                "septic_hookup":data["septic_hookup"],
                "assigned_parking":data["assigned_parking"],
                "tow_vehicle_parking":data["tow_vehicle_parking"],
                "trash_removal":data["trash_removal"],
                "pets_allowed":data["pets_allowed"],
                "internet_access":data["internet_access"]
            }

            location.amenity = Amenity.query.filter_by(
                electric_hookup = data["electric_hookup"],
                water_hookup = data["water_hookup"],
                septic_hookup = data["septic_hookup"],
                assigned_parking = data["assigned_parking"],
                tow_vehicle_parking = data["tow_vehicle_parking"],
                trash_removal = data["trash_removal"],
                pets_allowed = data["pets_allowed"],
                internet_access = data["internet_access"]).first() if None else Amenity(**amenity_data)

            necessity_data = {
                "rv_compatible":data["rv_compatible"],
                "generators_allowed":data["generators_allowed"],
                "fires_allowed":data["fires_allowed"],
                "max_days":data["max_days"],
                "pad_type":data["pad_type"],
            }

            location.necessity = Necessity.query.filter_by(
                rv_compatible = data["rv_compatible"],
                generators_allowed = data["generators_allowed"],
                fires_allowed = data["fires_allowed"],
                max_days = data["max_days"],
                pad_type = data["pad_type"]).first() if None else Necessity(**necessity_data)

            db.session.commit()

            return {"message": "Locations was successfully updated!"}
        else:
            return {"message": "Locations not found!"}, 404

    def delete(self, id):
        '''Delete Location record for the provided location id'''
        location = Location.query.get(int(id))
        if location:
            db.session.delete(location)
            db.session.commit()
            return {"message": "Location deleted successfully."}
        else:
            return {"message": "Locations not found!"}, 404
