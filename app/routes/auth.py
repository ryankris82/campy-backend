from flask import Blueprint, redirect, url_for, request, jsonify
from app.models.models import db, User
from flask_jwt_extended import  JWTManager, jwt_required, create_access_token
from flask_restx import Api, Resource, Namespace, fields



bp = Blueprint("auth", __name__)
api = Api(bp)

signup_model = api.model("Registration", {
                            "firstName": fields.String("User first name."),
                            "lastName": fields.String("User last name."),
                            "email": fields.String("Unique email address."),
                            "password": fields.String("User Password."),
                            "domicileType": fields.String("User domicile type."),
                            "phoneNumber": fields.String("User phone number."),
                            })

login_model = api.model("Login", {
                            "email": fields.String("Unique email address."),
                            "password": fields.String("User Password."),
                            })

@api.route("/signup")
class Signup(Resource):
    @api.expect(signup_model)
    def post(self):
        email = api.payload["email"]
        password = api.payload["password"]

        test = User.query.filter_by(email=email).first()
        if test:
            return {"message": "The email already is registered"} , 409
        else:
            password = api.payload["password"]
            first_name = api.payload["firstName"]
            last_name = api.payload["lastName"]
            domicile_type = api.payload["domicileType"]
            phoneNumber = api.payload["phoneNumber"]
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                domicile_type=domicile_type,
                phone_number=phoneNumber
                )

            db.session.add(user)
            db.session.commit()
            return {"message": "successfully created user."}, 201

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        email = api.payload["email"]
        password = api.payload["password"]

        user = User.query.filter_by(email=email).first()

        if  user:
            valid= user.check_password(password)
            if valid:
                access_token = create_access_token(identity=email)
                return {
                    "access_token":access_token,
                    "user_id":user.id,
                    "user_first_name":user.first_name,
                    "user_last_name":user.last_name,
                }
        else:
            return { "message":  "Bad email or password."} , 401
