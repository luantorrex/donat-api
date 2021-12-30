from app import app 
from app.dataConsumer import consumingDataPerDate as dpd
from app.initials import initialsToState
from app.news import callGoogle
from datetime import date, timedelta
import json
# import bcrypt
from flask_restful import Api, Resource, reqparse
# from flask_cors import CORS #comment this on deployment
from flask import redirect, url_for, request, jsonify, render_template, session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")

api = Api(app)


# @app.route('/api/state/<string:state>')
# @app.route('/api/state/<string:state>/<string:day>')
# def showState(state,day=defaultDay):
#     state = state.upper()
#     data = dpd(day)
#     return str(data[state])

# @app.route('/api/date')
# @app.route('/api/date/<string:day>')
# def showDate(day=defaultDay):
#     data = dpd(day)
#     #import ipdb; ipdb.set_trace()
#     return str(data)



# @app.route('/api/state/<string:state>')
# @app.route('/api/state/<string:state>/<string:day>')
# def showState(state,day=defaultDay):
#     state = state.upper()
#     data = dpd(day)
#     return str(data[state])

# @app.route('/api/date')
# @app.route('/api/date/<string:day>')
# def showDate(day=defaultDay):
#     data = dpd(day)
#     #import ipdb; ipdb.set_trace()
#     return str(data)


@app.route('/api/news')
@app.route('/api/news/<string:state>')
def showNews(state='Brasil'):
    state = state.upper()
    if state not in initialsToState:
        state = 'Brasil'
    else:
        state = initialsToState[state]
    return str(callGoogle(state))

# class Instituicao(Resource):
#     def get(self):
#         instituicao = inst.query.all()
#         return instituicao

#     def post(self):
#         try:
#             name = request.json.get('name', None)
#             email = request.json.get('email', None)
#             address = request.json.get('address', None)
#             url = request.json.get('url', None)
#             phone_number = request.json.get('phone_number', None)

#             instituicao = inst(
#                 name=name, email=email, address=address, url=url, phone_number=phone_number)

#             db.session.add(instituicao)
#             db.session.commit()

#             return "Registered!"

#         except IntegrityError:
#             return "Integrity Error", 400


# api.add_resource(Instituicao, '/api/instituicao')


# class InstituicaoById(Resource):
#     def get(self, id):
#         instituicao = inst.query.filter_by(id=id).first()
#         return instituicao

#     def post(self):
#         try:
#             name = request.json.get('name', None)
#             email = request.json.get('email', None)
#             address = request.json.get('address', None)
#             url = request.json.get('url', None)
#             phone_number = request.json.get('phone_number', None)

#             instituicao = inst(
#                 name=name, email=email, address=address, url=url, phone_number=phone_number)

#             db.session.add(instituicao)
#             db.session.commit()

#             return "Registered!"
#         # melhor forma de fazer o except
#         # ele da except tanto quando os mesmos dados são passados, tanto quando falta algum atributo.
#         except IntegrityError:
#             return "Integrity Error", 400


# api.add_resource(InstituicaoById, '/api/instituicao/<string:id>')


class Register(Resource):
    def post(self): 
        name = request.json.get('full_name', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        address = request.json.get('address', None)
        phone_number = request.json.get('phone_number', None)
        gender = request.json.get('gender', None)

        user_found = User.objects(full_name__in=[name]).first()
        email_found = User.objects(email__in=[email]).first()

        if user_found:
            return 'There already is a user by that name'
        if email_found:
            return 'This email already exists in database'
        else:
            user_input = User(full_name = name, email= email, password = generate_password_hash(password), address = address, phone_number = phone_number, gender = gender)            
            user_input.save()
            return jsonify({'result': 'User created!'})

api.add_resource(Register, '/api/register')


class Login(Resource):
    def post(self):
        try:
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            
            if not email:
                return 'Missing e-mail!', 400
            if not password:
                return 'Missing Password!', 400

            user_found = User.objects(email__in=[email]).first()

            if not user_found:
                return 'User Not Found!', 404
            
            if check_password_hash(user_found.password, password):
                session['logged_in'] = True
                status = True         
            else:
                status = False
            return jsonify({'result': status})
        except:
            return "Please provide an email and a password", 400

api.add_resource(Login, '/api/login')


class Logout(Resource):
    def post(self):
        session.pop('logged_in', None)
        return jsonify({'result': 'success'})

api.add_resource(Logout, '/api/logout')