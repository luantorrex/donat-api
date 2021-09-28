from app import app, db
from app.dataConsumer import consumingDataPerDate as dpd
from app.initials import initialsToState
from app.news import callGoogle
from app.models import User as u,Instituicao as inst, UserSchema
from datetime import date, timedelta
import json
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from flask import redirect, url_for, request, jsonify
from sqlalchemy.exc import IntegrityError


defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")

CORS(app) #comment this on deployment
api = Api(app)


@app.route('/api/state/<string:state>')
@app.route('/api/state/<string:state>/<string:day>')
def showState(state,day=defaultDay):
    state = state.upper()
    data = dpd(day)
    return str(data[state])

@app.route('/api/date')
@app.route('/api/date/<string:day>')
def showDate(day=defaultDay):
    data = dpd(day)
    #import ipdb; ipdb.set_trace()
    return str(data)


@app.route('/api/news')
@app.route('/api/news/<string:state>')
def showNews(state='Brasil'):
    state = state.upper()
    if state not in initialsToState:
        state = 'Brasil'
    else:
        state = initialsToState[state]
    return str(callGoogle(state))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
class User(Resource):
    def get (self):
        print('teste')
        all_users = u.query.all()
        return jsonify(users_schema.dump(all_users))
        # return jsonify(result)
    # def post (self):
    #     name = request.json.get('full_name', None)
    #     email = request.json.get('email', None)
    #     password = request.json.get('password_hash', None)
    #     address = request.json.get('address', None)
    #     gender = request.json.get('gender', None)
    #     phone_number = request.json.get('phone_number', None)
    #     user = u(full_name=name, email=email, password_hash=password, address=address, gender=gender, phone_number=phone_number)
    #     db.session.add(user)
    #     db.session.commit()
    #     return jsonify(user_schema.dump(user))    

api.add_resource(User, '/api/user')

class UserById(Resource):
    def get (self,id):
        print('teste')
        user = u.query.filter_by(id=id)
        return jsonify(user_schema.dump(user))
    

api.add_resource(UserById, '/api/user/<string:id>')
class Instituicao(Resource):
    def get (self):
        inst = inst.query.all()
        return inst

api.add_resource(Instituicao, '/api/instituicao')
class InstituicaoById(Resource):
    def get (self, id):
        inst = inst.query.filter_by(id=id).first()
        return inst

    def post (self):
        try:
            name = request.json.get('name', None)
            email = request.json.get('email', None)
            address = request.json.get('address', None)
            phone_number = request.json.get('phone_number', None)


            instituicao = Instituicao(name=name, email=email, address=address, phone_number=phone_number)
            
            db.session.add(instituicao)
            db.session.commit()
            
            return "Registered!"
        # melhor forma de fazer o except
        # ele da except tanto quando os mesmos dados são passados, tanto quando falta algum atributo.    
        except IntegrityError:
            return "Integrity Error",400

api.add_resource(InstituicaoById, '/api/instituicao/<string:id>')
class Register(Resource):
    # def get (self):
    #     users = User.query.all()
    #     # print(users.id)
    #     # users.password_hash.decode('utf-8')
    #     return jsonify(users)
    def post (self):
        try:
            name = request.json.get('name', None)
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            address = request.json.get('address', None)
            gender = request.json.get('gender', None)


            user = u(full_name=name, email=email, password_hash=password, address=address, gender=gender)
            
            db.session.add(user)
            db.session.commit()
            
            return "Registered!"
        # melhor forma de fazer o except
        # ele da except tanto quando os mesmos dados são passados, tanto quando falta algum atributo.    
        except IntegrityError:
            return "Integrity Error",400


api.add_resource(Register, '/api/register')


# @app.route('/login/', methods=['GET', 'POST'])
class Login(Resource):
        def post(self):
            try:
                email = request.json.get('email', None)
                password = request.json.get('password', None)

                if not email:
                    return 'Missing e-mail!', 400
                if not password:
                    return 'Missing Password!', 400
            
                user = u.query.filter_by(email=email).first()

                if not user:
                    return 'User Not Found!', 404
            
                if (password == user.password_hash):
                    return f'Welcome back {user.full_name}'
                return "Wrong Password!"
            except :
               return "Please provide an email and a password", 400

api.add_resource(Login, '/api/login')

@app.route('/api/logout')
def logout():
    return redirect(url_for('index'))