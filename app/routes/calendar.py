from app.models.models import db, Calendar, Location, Necessity
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
    @api.param('location_id', 'The location identifier')
    def get(self, location_id):
        '''Get all Calendar Bookings'''
        dates = Calendar.query.filter_by(location_id=location_id).all()

        data = [day.to_dictionary() for day in dates]

        return {"dates": data}

    # @api.expect(model)
    def post(self, location_id):
        '''Create a new calendar booking with the provided date range'''
        print(api.payload)
        data = api.payload
        dates = Calendar.query.filter_by(location_id=location_id).all()

        if bool(dates) == False:
            calendar = Calendar(**data)
            db.session.add(calendar)
            db.session.commit()
            return {"message": "Successfully scheduled!"}, 200
        else:
            # get the api payload data for the requested start and end date and convert to datetime from string
            req_start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            req_end_date = datetime.datetime.strptime(data["end_date"], "%Y-%m-%d").date()

            # make sure the start day is actually before the end date!!!
            if (req_start_date > req_end_date):
                return {"message": "You must choose a start date before your end date"}, 202

            # get the max_days for the location and the number of days requested to schedule
            max_days = check_max_days(location_id)
            num_of_days_scheduled = get_num_of_days_scheduled(req_start_date, req_end_date)

            # send a helpful message if the days scheduled exceed the max_days allowed for a stay
            if(num_of_days_scheduled > max_days):
                return {"message": f"Your requested stay is too long. The max number if days allowed here is {max_days}. You scheduled for {num_of_days_scheduled}"}, 202

            # check each scheduled date for any overlap with the requested dates
            # Czechy way of invoking the helper function
            if check_for_overlap(dates, req_start_date, req_end_date):
                return check_for_overlap(dates, req_start_date, req_end_date)

            # if the requested dates do not envelope or are enveloped by an existing date range, commit the selected dates to the database
            calendar = Calendar(**data)
            db.session.add(calendar)
            db.session.commit()
            return {"message": "Successfully scheduled!"}, 200

@api.route("/<int:id>")
@api.response(404, "Calendar Booking not found")
@api.param('id', 'The calendar identifier')
@api.param('location_id', 'The location identifier')
class CalendarById(Resource):
    def get(self, location_id, id):
        '''Get a Calendar date for the provided id'''
        calendar_range = Calendar.query.get(int(id))
        if calendar_range:
            return {"calendar":calendar_range.to_dictionary()}
        else:
            return {"message": "Calendar Entry Not Found"}, 404
    @api.expect(model)
    def put(self, location_id, id):
        '''Update calendar by calendar id using the data passed in'''
        # get the specifc calendar date to edit
        calendar_range = Calendar.query.get(int(id))
        # get all the dates for the object to update on
        database_dates = Calendar.query.filter_by(location_id=location_id).all()

        # make sure the database entry compared against the update value does not trip up

        if calendar_range:
            data = api.payload

            # convert the start and end datetimes into comparable dates
            req_start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            req_end_date = datetime.datetime.strptime(data["end_date"], "%Y-%m-%d").date()

            # make sure the start day is actually before the end date!!!
            if (req_start_date > req_end_date):
                return {"message": "You must choose a start date before your end date"}, 202

            max_days = check_max_days(location_id)
            num_of_days_scheduled = get_num_of_days_scheduled(req_start_date, req_end_date)

            # compare the number of days scheduled to the max number of days allowed
            if num_of_days_scheduled > max_days:
                return {"message": f"Your requested stay is too long. The max number if days allowed here is {max_days}. You scheduled for {num_of_days_scheduled}"}, 202

            # check each scheduled date for any overlap with the requested dates
            if check_for_overlap(database_dates, req_start_date, req_end_date):
                return check_for_overlap(database_dates, req_start_date, req_end_date)

            # assign the payload data to overwrite the old start and end date data
            calendar_range.start_date = req_start_date
            calendar_range.end_date = req_end_date

            db.session.commit()

            return {"message": "Calendar Booking was successfully updated!"}, 200
        else:
            return {"message": "Calendar Booking was not found"}, 404

    def delete(self, location_id, id):
        '''Delete Calendar Booking for the provided calendar id'''
        calendar_range = Calendar.query.get(int(id))
        if calendar_range:
            db.session.delete(calendar_range)
            db.session.commit()
            return {"message": "Calendar Booking deleted successfully"}, 200
        else:
            return {"message": "Calendar Booking not found, nothing deleted"}, 404

# helper methods
def check_max_days(location_id):
    location = Location.query.filter_by(id=location_id).one()
    necessity = Necessity.query.filter_by(id=location.necessity_id).one()
    max_days = necessity.max_days
    return max_days

def get_num_of_days_scheduled(sd, ed):
    days = []
    day = sd
    while day <= ed:
        days.append(day)
        day += datetime.timedelta(days=1)
    return len(days)

def check_for_overlap(dates, req_start_date, req_end_date):
    for date in dates:
        start = date.start_date
        end = date.end_date
                                        # checks if the req time is within an existing time block                    # checks if the req time envelopes an existing time block
        if (req_start_date >= start and req_start_date <= end) or (req_end_date >= start and req_end_date <= end) or (req_start_date <= start and req_end_date >= end):
            return {"message": "Chosen date range is unavailable"}, 202
    # Good idea to find a better way of handling this
    return False
