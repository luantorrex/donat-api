from app import app 
from app.dataConsumer import consumingDataPerDate as dpd
from app.initials import initialsToState
from app.news import callGoogle
from datetime import date, timedelta
import json
from flask_restful import Api, Resource, reqparse
from flask import request, jsonify, session
from app.models import User, Instituicao
from werkzeug.security import generate_password_hash, check_password_hash


defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")

api = Api(app)


@app.route("/api/news")
@app.route("/api/news/<string:state>")
def showNews(state="Brasil"):
    state = state.upper()
    if state not in initialsToState:
        state = "Brasil"
    else:
        state = initialsToState[state]
    return str(callGoogle(state))

class Institution(Resource):
    def get(self):
        data = []

        for inst in Instituicao.objects:
            data.append({
                "email": inst.email,
                "name": inst.name,
                "address": inst.address,
                "url": inst.url,
                "cep": inst.cep,
                "phone_number": inst.phone_number
            })

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        
        return response

    def post(self):
        body = json.loads(request.data)

        name = body.get("name", None)
        email = body.get("email", None)
        address = body.get("address", None)
        url = body.get("url", None)
        cep = body.get("cep", None)
        phone_number = body.get("phone_number", None)
        
        name_found = Instituicao.objects(name__in=[name]).first()
        email_found = Instituicao.objects(email__in=[email]).first()

        if name_found:
            return "There already is a institution by that name"
        if email_found:
            return "This email already exists in database"
        else:
            institution_input = Instituicao(name=name, email=email, address=address, url=url, cep=cep, phone_number=phone_number)            
            institution_input.save()
            return jsonify({"result": "Institution created!"})

api.add_resource(Institution, "/api/instituicao")


class InstituicaoById(Resource):
    def get(self, email):
        instituicao = Instituicao.objects(email__in=[email]).first()
        return instituicao.to_json()


api.add_resource(InstituicaoById, "/api/instituicao/<string:email>")


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
            return "There already is a user by that name"
        if email_found:
            return "This email already exists in database"
        else:
            user_input = User(full_name = name, email= email, password = generate_password_hash(password), address = address, phone_number = phone_number, gender = gender)            
            user_input.save()
            return jsonify({"result": "User created!"})

api.add_resource(Register, "/api/register")


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email", None)
            password = request.json.get("password", None)
            
            if not email:
                return "Missing e-mail!", 400
            if not password:
                return "Missing Password!", 400

            user_found = User.objects(email__in=[email]).first()

            if not user_found:
                return "User Not Found!", 404
            
            if check_password_hash(user_found.password, password):
                session["logged_in"] = True
                status = True         
            else:
                status = False
            return jsonify({"result": status})
        except:
            return "Please provide an email and a password", 400

api.add_resource(Login, "/api/login")


class Logout(Resource):
    def post(self):
        session.pop("logged_in", None)
        return jsonify({"result": "success"})

api.add_resource(Logout, "/api/logout")