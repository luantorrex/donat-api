from http import HTTPStatus
from http.client import OK
import json
from flask_restful import Resource
from flask import Response, request, jsonify 
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, unset_jwt_cookies, create_refresh_token, set_refresh_cookies, get_jwt_identity, set_access_cookies,jwt_required
)
from PIL import Image as PImage
# from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

class Register(Resource):
    def post(self):
        body = json.loads(request.data)
        
        name = body.get("username", None)
        email = body.get("email", None)
        password = body.get("password", None)
        address = body.get("address", None)
        phone_number = body.get("phone_number", None)
        gender = body.get("gender", None)

        user_found = User.objects(username__in=[name]).first()
        email_found = User.objects(email__in=[email]).first()

        if user_found:
            return Response("There already is a user by that name", mimetype="application/json", status=400)
        if email_found:
            return Response("This email already exists in database", mimetype="application/json", status=400)
        else:
            user_input = User(username = name, email= email, password = generate_password_hash(password), address = address, phone_number = phone_number, gender = gender)
            my_image = open('./assets/images/icon.png', 'rb')
            user_input.icon.replace(my_image, filename="icon.jpg")
            
            # image = PImage.open(r'./assets/images/icon.png')
            # image.show()
            # print(image)
            # user_input.icon.put(image)
            # print(user_input.icon)
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
                response = jsonify()
                access_token = create_access_token(identity=str(user_found.pk),fresh=True)
                refresh_token = create_refresh_token(identity=user_found)
                response = jsonify(
                    {
                        "data": {
                            "user_id": str(user_found.pk),
                            "user_name": user_found.username,
                            "email": user_found.email,
                        },
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                    )  
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            else:
                return Response("Review your Input", mimetype="application/json", status=404)
        except:
            return Response("Something goes wrong", mimetype="application/json", status=500)


class Logout(Resource):
    @jwt_required()
    def post(self):
        response = jsonify({'message': 'Successfully logged out'})
        unset_jwt_cookies(response)
        return response


class RefreshAccessTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        if current_user:
            token = create_access_token(identity=current_user, fresh=False)
            return {'token': token}, HTTPStatus.OK
        return {"message": "invalid user"}, HTTPStatus.UNAUTHORIZE   