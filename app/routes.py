from app import app, db
from app.dataConsumer import consumingDataPerDate as dpd
from app.initials import initialsToState
from app.news import callGoogle
from app.models import User
from datetime import date, timedelta
import json
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from flask import redirect, url_for, request, jsonify
import bcrypt
from sqlalchemy.exc import IntegrityError


defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")

CORS(app) #comment this on deployment
api = Api(app)


@app.route('/state/<string:state>/')
@app.route('/state/<string:state>/<string:day>/')
def showState(state,day=defaultDay):
    state = state.upper()
    data = dpd(day)
    return str(data[state])


@app.route('/general/')
@app.route('/date/')
@app.route('/date/<string:day>/')
def showDate(day=defaultDay):
    data = dpd(day)
    #import ipdb; ipdb.set_trace()
    return str(data)


@app.route('/news/')
@app.route('/news/<string:state>/')
def showNews(state='Brasil'):
    state = state.upper()
    if state not in initialsToState:
        state = 'Brasil'
    else:
        state = initialsToState[state]
    return str(callGoogle(state))

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

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user = User(full_name=name, email=email, password_hash=hashed, address=address, gender=gender)
            
            db.session.add(user)
            db.session.commit()
            
            return "Registered!"
        # melhor forma de fazer o except
        # ele da except tanto quando os mesmos dados são passados, tanto quando falta algum atributo.    
        except IntegrityError:
            return "Integrity Error",400

api.add_resource(Register, '/register')


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
            
                user = User.query.filter_by(email=email).first()

                if not user:
                    return 'User Not Found!', 404
            
                if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                    return f'Welcome back {user.full_name}'
                return "Wrong Password!"
            except :
               return "Please provide an email and a password", 400

api.add_resource(Login, '/login')

@app.route('/logout/')
def logout():
    return redirect(url_for('index'))