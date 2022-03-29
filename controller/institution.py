from http import HTTPStatus
import json
from flask_restful import Resource
from helper.map_converter import AddressToLagLong
from flask import Response, jsonify, request
from flask_jwt_extended import jwt_required
from database.models import Instituicao
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
        name = body.get("name", None)
        email = body.get("email", None)
        address = body.get("address", None)
        institution_type = body.get("institution_type", None)
        url = body.get("url", None)
        cep = body.get("cep", None)
        image = body.get("image", None)
        phone_number = body.get("phone_number", None)
        
        name_found = Instituicao.objects(name__in=[name]).first()
        email_found = Instituicao.objects(email__in=[email]).first()

        if name_found:
            return Response("There already is a institution by that name", mimetype="application/json", status=400)
        if email_found:
            return Response("This email already exists in database", mimetype="application/json", status=400)
        else:
            institution_input = Instituicao(name=name, email=email, address=address, institution_type= institution_type, url=url, cep=cep, image=image ,phone_number=phone_number)
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
            "image": instituicao['image'],
            "institution_type": instituicao['institution_type'].value,
            "phone_number":instituicao['phone_number'],
            "latitude": lag_long.latitude,
            "longitude": lag_long.longitude
        }
        print(response)
        return response
