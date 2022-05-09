from http import HTTPStatus
import io
from flask import jsonify, request, send_file
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
                            "full_name": user.full_name,
                            "email": user.email,
                            "phone_number": user.phone_number,
                        },
                    }
                    )  
            return response 
        return {"status":"fail"}, HTTPStatus.UNAUTHORIZED
    
class profileImage(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = User.objects.get(pk=identity)
        
        icon= user.icon.read()
        filename = user.icon.filename
        content_type = user.icon.content_type
        return send_file(io.BytesIO(icon), 
                        attachment_filename=filename, 
                        mimetype=content_type)
        
    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        user = User.objects.get(pk=identity)

        image = request.files['icon']
        
        user.icon.replace(image, content_type = 'image/jpeg')
        user.save()
            