from app.models.models import db, Review, Location
from flask_restx import Resource, Namespace, fields


api = Namespace('reviews', description='Create, update and delete location reviews')

model = api.model("Review",
                        {
                        "overall_rating": fields.Integer(required=True, description="Location overall rating."),
                        "noise": fields.Integer(required=True, description="Location Noise level."),
                        "safety": fields.Integer(required=True, description="Location Safety level."),
                        "cleanliness": fields.Integer(required=True, description="Location cleanliness level."),
                        "access": fields.Integer(required=True, description="Location easy of access."),
                        "site_quality": fields.Integer(required=True, description="Location site quality."),
                        "user_id": fields.Integer(required=True, description="Reviewer Id."),
                        "comments": fields.String(required=True, description="User's comments on the location")
                        }
                )


@api.route("/")
@api.response(404, 'Review not found')
@api.param('location_id', 'The location identifier')
class Reviews(Resource):
    def get(self, location_id):
        '''Get all the reviews for the location'''
        reviews = Review.query.filter_by(location_id=location_id).all()
        data = [review.to_dictionary() for review in reviews]
        return {"reviews": data}

    @api.expect(model)
    def post(self, location_id):
        '''Create a new review for the location'''
        data = api.payload
        data["location"] = Location.query.get(int(location_id))
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        return {"message": "Review successfully submitted!"}


@api.route("/<int:id>")
@api.response(404, 'Review not found')
@api.param('id', 'The review identifier')
@api.param('location_id', 'The location identifier')
class ReviewsById(Resource):
    @api.expect(model)
    def put(self, location_id, id):
        '''Update review by the provided id using the data passed in'''
        data=api.payload
        review = Review.query.get(int(id))
        if review:
            review.overall_rating = data["overall_rating"]
            review.noise = data["noise"]
            review.safety = data["safety"]
            review.cleanliness = data["cleanliness"]
            review.access = data["access"]
            review.site_quality = data["site_quality"]
            review.comments = data["comments"]
            db.session.commit()
            return {"message": "Review was successfully updated!"}
        else:
            return {"message": "Locations not found!"}, 404


    def delete(self, location_id, id):
        '''Delete Review record for the provided location id'''
        review = Review.query.get(int(id))
        if review:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Review successfully deleted!"}
        else:
            return {"message": "Review not found!"}, 404
