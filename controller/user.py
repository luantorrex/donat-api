from http import HTTPStatus
from flask import jsonify
from flask_restful import Resource

from database.models import User
from flask_jwt_extended import get_jwt_identity, jwt_required


class getLoggedUser(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = User.objects.get(pk=identity)
        if user:
            response = jsonify(
                    {
                        "data": {
                            'message':"testando usuario nessa bagaça",
                            "id": str(user.pk),
                            "username": user.username,
                            "email": user.email,
                            "address": user.address,
                            "phone_number": user.phone_number,
                            "gender": str(user.gender.value)
                        },
                    }
                    )  
            return response 
        return {"status":"fail"}, HTTPStatus.UNAUTHORIZED
    