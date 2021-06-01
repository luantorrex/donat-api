from app import app
from app.dataConsumer import consumingData, consumingDataPerDate as dpd
from datetime import date,timedelta

defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/general')
def showCountry():
    data = consumingData()
    return str(data)


@app.route('/state/<string:state>')
def showState(state):
    state = state.upper()
    data = consumingData()
    return str(data[state])


@app.route('/date/')
@app.route('/date/<string:day>')
def showDate(day=defaultDay):
    data = dpd(day)
    #import ipdb; ipdb.set_trace()
    return str(data)
