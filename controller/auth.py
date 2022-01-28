import json
from logging import error
from flask_restful import Resource
from flask import Response, request, jsonify, session
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
# from helper.errors import EmailAlreadyExistsError, InternalServerError, MissingInputError, UnauthorizedError, UserExistsError
# from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

class Register(Resource):
    def post(self): 
        body = json.loads(request.data)
        
        name = body.get("full_name", None)
        email = body.get("email", None)
        password = body.get("password", None)
        address = body.get("address", None)
        phone_number = body.get("phone_number", None)
        gender = body.get("gender", None)

        user_found = User.objects(full_name__in=[name]).first()
        email_found = User.objects(email__in=[email]).first()

        if user_found:
            return Response("There already is a user by that name", mimetype="application/json", status=400)
        if email_found:
            return Response("This email already exists in database", mimetype="application/json", status=400)
        else:
            user_input = User(full_name = name, email= email, password = generate_password_hash(password), address = address, phone_number = phone_number, gender = gender)            
            user_input.save()
            return Response("User created", mimetype="application/json", status=201)


class Login(Resource):
    def post(self):
        try:
            body = json.loads(request.data)

            email = body.get("email", None)
            password = body.get("password", None)
            
            if not email or not password:
                return Response("Don't leave any field in blank", mimetype="application/json", status=400)

            user_found = User.objects(email__in=[email]).first()

            if not user_found:
                return Response("User not Found", mimetype="application/json", status=404)
                        
            if check_password_hash(user_found.password, password):
                session["logged_in"] = True
                return Response("Logged In", mimetype="application/json", status=200)
            else:
                return Response("Review your Input", mimetype="application/json", status=404)
        except:
            return Response("Something goes wrong", mimetype="application/json", status=500)


class Logout(Resource):
    def post(self):
        session.pop("logged_in", None)
        return Response("Logged Out", mimetype="application/json", status=200)