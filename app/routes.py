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

@app.route('/login/', methods=['GET', 'POST'])
def login():
   return "Login!"

@app.route('/logout/')
def logout():
    return redirect(url_for('index'))

class Register(Resource):
    def get (self):
        users = User.query.all()
        print(users)
        return jsonify(users)


    def post (self):
        name = request.json.get('name', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        address = request.json.get('address', None)
        gender = request.json.get('gender', None)

        user = User(full_name=name, email=email, password_hash=password, address=address, gender=gender)
        
        db.session.add(user)
        db.session.commit()

        return "Register!"

api.add_resource(Register, '/register')
