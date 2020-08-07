from app.models.models import db, Calendar
from flask_restx import Resource, Namespace, fields
import datetime

api = Namespace('calendar', description='Calendar operations')

# expected information
model = api.model("Calendar",
                {
                    "start_date": fields.Date(required=True, description="Calendar start date"),
                    "end_date": fields.Date(required=True, description="Calendar end date"),
                    "location_id": fields.Integer(required=True, description="Calendar location", example=1),
                    "user_id": fields.Integer(required=True, description="Calendar user", example=1),
                }
)

@api.route("/")
class Calendars(Resource):
    '''Get all Scheduled Calendar Ranges'''
    def get(self, location_id):
        '''Get all Calendar Bookings'''
        dates = Calendar.query.filter_by(location_id=location_id).all()

        data = [day.to_dictionary() for day in dates]

        return {"dates": data}

    @api.expect(model)
    def post(self, location_id):
        '''Create a new calendar booking with the provided date range'''
        data = api.payload
        dates = Calendar.query.filter_by(location_id=location_id).first()
        start = dates.start_date
        end = dates.end_date

        print("Start", start)

        if bool(dates) == False:
            calendar = Calendar(**data)
            db.session.add(calendar)
            db.session.commit()
            return {"Message": "Successfully scheduled!"}
        else:
            # get the calendar entries for a given location
            locationDates = Calendar.query.filter_by(location_id=location_id).all()
            # get the api payload data for the requested start and end date and convert to datetime from string
            req_start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            req_end_date = datetime.datetime.strptime(data["end_date"], "%Y-%m-%d").date()

            for date in locationDates:
                start = date.start_date
                end = date.end_date
                                                # checks if the req time is within an existing time block                    # checks if the req time envelopes an existing time block
                if (req_start_date >= start and req_start_date <= end) or (req_end_date >= start and req_end_date <= end) or (req_start_date <= start and req_end_date >= end):
                    return {"Message": "Chosen date range is unavailable"}
            # if the requested dates do not envelope or are enveloped by an existing date range, commit the selected dates to the database
            calendar = Calendar(**data)
            db.session.add(calendar)
            db.session.commit()
            return {"Message": "Successfully scheduled!"}

    @api.routes("/<int:id>")
    @api.response(404, "Calendar Booking not found")
    class CalednarById(Resource):
        def get(self, id):
            '''Get a Calendar date for the provided id'''
            calendar_range = Calendar.query.get(int(id))
            if calendar_range:
                return {"calendar":calendar_range.to_dictionary()}
            else:
                return {"message": "Calendar Entry Not Found"}, 404
        @api.expect(model)
        def put(self, id):
            '''Update calendar by calendar id using the data passed in'''
            calendar_range = Calendar.query.get(int(id))
            if calendar_range:
                data = api.payload

                calendar_range.start_date = data["start_date"]
                calendar_range.end_date = data["end_date"]

                db.session.commit()

                return {"message": "Calendar Booking was successfully updated!"}
            else:
                return {"message": "Calendar Booking was not found"}, 404

        def delete(self, id):
            '''Delete Calendar Booking for the provided calendar id'''
            calendar_range = Calendar.query.get(int(id))
            if calendar_range:
                db.session.delete(calendar_range)
                db.session.commit()
                return {"message": "Calendar Booking deleted successfully"}
            else:
                return {"message": "Calendar Booking not found, nothing deleted"}, 404
