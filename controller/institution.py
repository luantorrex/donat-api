from http import HTTPStatus
import io
import json
from flask_restful import Resource
from helper.map_converter import AddressToLagLong
from flask import Response, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from database.models import Instituicao, RequestInstitution
# from helper.errors import EmailAlreadyExistsError, InstitutionExistsError
import re

from helper.map_converter import AddressToLagLong

def remove_oid(string):
    while True:
        pattern = re.compile('{\s*"\$oid":\s*(\"[a-z0-9]{1,}\")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string

class Institution(Resource):
    @jwt_required()
    def get(self):
        instituicoes = Instituicao.objects().to_json()
        instituicoes = remove_oid(instituicoes)
        return Response(instituicoes, mimetype="application/json", status=200)
    
    @jwt_required()
    def post(self):
        body = json.loads(request.data)
        email = body.get("email", None)
        
        request_object = RequestInstitution.objects(email__in=[email]).first()
        obj = request_object.to_json()
        
        name = obj['name']
        address = obj['address']
        institution_type = obj['institution_type']
        url = obj['url']
        cep = obj['cep']
        phone_number = obj['phone_number']
        
        name_found = Instituicao.objects(name__in=[name]).first()
        email_found = Instituicao.objects(email__in=[email]).first()

        if name_found:
            return Response("There already is a institution by that name", mimetype="application/json", status=400)
        if email_found:
            return Response("This email already exists in database", mimetype="application/json", status=400)
        else:
            institution_input = Instituicao(name=name, email=email, address=address, institution_type= institution_type, url=url, cep=cep, phone_number=phone_number)
            institution_input.image.put(request_object.image, content_type = 'image/jpeg')
            institution_input.save()
            return jsonify(
                {
                    "message": "Institution created",
                    "status": HTTPStatus.CREATED
                }
            )  

class InstituicaoById(Resource):
    @jwt_required()
    def get(self, id):
        instituicao = Instituicao.objects.get(pk=id)
        lag_long = AddressToLagLong(instituicao['address'])
        response = {
            "name": instituicao['name'],
            "email": instituicao['email'],
            "address": instituicao['address'],
            "url": instituicao['url'],
            "cep": instituicao['cep'],
            "institution_type": instituicao['institution_type'].value,
            "phone_number":instituicao['phone_number'],
            "latitude": lag_long.latitude,
            "longitude": lag_long.longitude
        }
        return response

class RetrieveInstitutionImage(Resource):
    @jwt_required()
    def get(self, id): 
        instituicao = Instituicao.objects.get(pk=id)
        image = instituicao.image.read()
        filename = instituicao.image.filename
        content_type = instituicao.image.content_type
        return send_file(io.BytesIO(image), 
                        attachment_filename=filename, 
                        mimetype=content_type)


class RetrieveRandomInstitutions(Resource):
    def get(self):
        institutions = []
        instituicoes = Instituicao.objects().aggregate([{"$sample": { "size": 3 } },
                                                        {"$addFields": {"id": {"$toString": "$_id"}}},
                                                        {"$project": {"_id": 0, "image": 0}}])
        for document in instituicoes:
            institutions.append(document)
        return institutions
