from app.models.models import db, Review
from flask_restx import Resource, Namespace, fields


api = Namespace('reviews', description='Create and update location reviews')

@api.route("/")
class Reviews(Resource):
    def get(self, location_id):
        '''Get all the reviews for the location'''
        reviews = Review.query.filter(location_id==location_id).all()
        data = [review.to_dictionary() for review in reviews]
        return {"reviews": data}


# always have the url prefix consisting off a specific location and then /reviews
# bp = Blueprint("reviews", __name__, url_prefix="/location/<int:location_id>/reviews")

# @bp.route("/", methods=["GET"])
# def get_all_location_reviews(location_id):
#     # need to obtain the review by it"s location_id foreign key
#     reviews = Review.query.filter_by(location_id)
#     # jsonify all the reviews and return the jsonify
#     return jsonify(reviews)

# @bp.route("/<int:review_id>", methods=["GET"])
# def get_review_by_id(location_id, review_id):
#     # get review where the review"s location_id and id match the id provided in the url
#     review = Review.query.filter_by(Review.location_id == location_id and Review.id == review_id).one()
#     # return a review json object
#     return jsonify(review)

# @bp.route("/", methods=["POST"])
# def post_review(location_id):
#     # construct a review for a specific location
#     if request:
#         data = request # assign request to a shorter variable name that makes sense
#         # construct a review with the request data provided,
#         review = Review(
#             data.overall_rating,
#             data.noise,
#             data.safety,
#             data.cleanliness,
#             data.access,
#             data.site_quality,
#             data.comments,
#             data.createdAt,
#             data.updatedAt,
#             location_id=location_id, # assign location_id based on provided location_id
#         )
#         db.session.add(review)
#         db.session.commit()
#     else:
#         return jsonify("Bad Data")

# @bp.route("/<int:review_id>", methods=["PUT"])
# def edit_review(location_id, review_id):
#     # get review with given review_id
#     updateReview = Review.query.filter_by(Review.location_id == location_id and Review.id == review_id).one()
#     if request and updateReview:
#         data = request
#         updateReview = {
#             'overall_rating': data.overall_rating,
#             'noise': data.noise,
#             'safety': data.safety,
#             'cleanliness': data.cleanliness,
#             'access': data.access,
#             'site_quality': data.site_quality,
#             'comments': data.comments,
#             'createdAt': data.createdAt,
#             'updatedAt': data.updatedAt,
#         }
#         db.session.commit()
#     else:
#         return jsonify('Bad Data')

# @bp.route("/<int:review_id>", methods=["DELETE"])
# def delete_review(location_id, review_id):
#     # get the individual review
#     deleteReview = Review.query.filter_by(Review.location_id == location_id and Review.id == review_id).one()
#     # check if the request and deleteReview are valid
#     if request and deleteReview:
#         # delete deleteReview
#         db.session.delete(deleteReview)
#         # commit to db
#         db.session.commit()
#     else:
#         return jsonify("Deletion Failed")
