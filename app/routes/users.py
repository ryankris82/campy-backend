from app.models.models import db, User
from flask_restx import Resource, Namespace, fields

api = Namespace('users', description='Create and update user operations')

model = api.model("User", {
                            "firstName": fields.String( description="User first name.", example="John"),
                            "lastName": fields.String( description="User last name.", example="Doe"),
                            "userInfo": fields.String( description="User information.", example = "I love the oudoors"),
                            "domicileType": fields.String( description="User domicile type.", example = "RV"),
                            "phoneNumber": fields.String( description="User phone number.", example="555-555-5555"),
                            "password": fields.String( description="User Password.", example="password"),
                            "imageURL": fields.String( description="User Image URL.", example="/image.png"),
                         }
                )

@api.route("/<int:id>")
@api.param('id', 'User identifier')
@api.response(404, 'User not found')
@api.param('id', 'The user identifier')
class GetUser(Resource):
    @api.response(200, 'User found')
    @api.doc('get_user')
    def get(self, id):
        '''Get user by user id'''
        user = User.query.get(int(id))
        if user == None:
            return {"message": "no user found for the requested id"}, 404

        return {"user":user.to_dictionary()}


    @api.doc('update_user')
    @api.response(201, 'User record updated')
    @api.expect(model)
    def put(self, id):
        '''Update user record by user id'''
        user = User.query.get(int(id))
        if user == None:
            return {"message": "no user found for the requested id"}

        user.image_url = api.payload["imageURL"]
        user.phone_number = api.payload["phoneNumber"]
        user.user_info = api.payload["userInfo"]
        user.domicile_type = api.payload["domicileType"]
        user.first_name = api.payload["firstName"]
        user.last_name = api.payload["lastName"]
        db.session.commit()

        return {"message": "User record updated successfully."}
