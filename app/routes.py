from app import app
from app.dataConsumer import consumingData, jsonToDictPerData
from datetime import date,timedelta

defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/general')
def showCountry():
    test = consumingData()
    return str(test)


@app.route('/state/<string:state>')
def showState(state):
    state = state.upper()
    test = consumingData()
    return str(test[state])


@app.route('/date/')
@app.route('/date/<string:day>')
def showDate(day=defaultDay):
    test = jsonToDictPerData(day)
    #import ipdb; ipdb.set_trace()
    return str(test)
