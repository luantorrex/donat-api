from app import app
from app.dataConsumer import consumingDataPerDate as dpd
from datetime import date,timedelta

defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")


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


@app.route('/general')
@app.route('/date/')
@app.route('/date/<string:day>')
def showDate(day=defaultDay):
    data = dpd(day)
    #import ipdb; ipdb.set_trace()
    return str(data)
