from http import HTTPStatus
import io
import re
from textwrap import indent
from flask import Response, jsonify, request, send_file
from flask_restful import Resource
from itsdangerous import json

from database.models import RequestInstitution, User
from flask_jwt_extended import get_jwt_identity, jwt_required

def remove_oid(string):
    while True:
        pattern = re.compile('{\s*"\$oid":\s*(\"[a-z0-9]{1,}\")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string

class requestInstitutionHandler(Resource):
    
    @jwt_required()
    def get(self):
        request_institutions = RequestInstitution.objects().to_json()
        request_institutions = remove_oid(request_institutions)

        return Response(request_institutions, mimetype="application/json", status=HTTPStatus.OK)
    
    def put(self):
        email = request.form.get("email")
        image = request.files['icon']
        
        institution_input = RequestInstitution.objects(email__in=[email]).first()
        
        institution_input.image.replace(image, content_type = 'image/jpeg')
        institution_input.save()
    
    def post(self):
        body = json.loads(request.data)
        name = body.get("name")
        email = body.get("email")
        address = body.get("address")
        institution_type = body.get("institution_type")
        url = body.get("url")
        cep = body.get("cep")
        phone_number = body.get("phone_number")
        request_text = body.get("request_text")
        
        email_found = RequestInstitution.objects(email__in=[email]).first()
        
        if email_found:
            return Response("This email already exists in database", mimetype="application/json", status=HTTPStatus.BAD_REQUEST)
        else:
            institution_input = RequestInstitution(name=name, email=email, address=address, institution_type= institution_type, url=url, cep=cep ,phone_number=phone_number, request_text=request_text)
            my_image = open('./assets/images/icon.png', 'rb')
            institution_input.image.replace(my_image, filename="image.jpg")
            institution_input.save()
            return jsonify(
                {
                    "message": "Saved in database",
                    "status": HTTPStatus.CREATED
                }
            )  

class requestInstitutionImage(Resource):
    @jwt_required()
    def get(self, id):
        institution = RequestInstitution.objects.get(pk=id)
        image= institution.image.read()
        filename = institution.image.filename
        content_type = institution.image.content_type
        return send_file(io.BytesIO(image), 
                        attachment_filename=filename, 
                        mimetype=content_type)
      
class deleteInstitutionRequestById(Resource):
    
    @jwt_required()
    def delete(self, id):
        institution = RequestInstitution.objects.get(pk=id)
        institution.delete()
        return Response(mimetype="application/json", status=HTTPStatus.OK)