from app import app
from app.dataConsumer import consumingDataPerDate as dpd
from app.initials import initialsToState
from app.news import callGoogle
from datetime import date,timedelta
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment

defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")

CORS(app) #comment this on deployment
api = Api(app)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/state/<string:state>')
@app.route('/state/<string:state>/<string:day>')
def showState(state,day=defaultDay):
    state = state.upper()
    data = dpd(day)
    return str(data[state])


@app.route('/general/')
@app.route('/date/')
@app.route('/date/<string:day>')
def showDate(day=defaultDay):
    data = dpd(day)
    #import ipdb; ipdb.set_trace()
    return str(data)


@app.route('/news/')
@app.route('/news/<string:state>')
def showNews(state='Brasil'):
    state = state.upper()
    if state not in initialsToState:
        state = 'Brasil'
    else:
        state = initialsToState[state]
    return str(callGoogle(state))