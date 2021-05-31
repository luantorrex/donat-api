from app import app
from app.dataConsumer import consumingData


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/general')
def showCountry():
    test = consumingData()
    #import ipdb; ipdb.set_trace()
    return str(test)

@app.route('/general/<string:state>')
def showState(state):
    state = state.upper()
    test = consumingData()
    #import ipdb; ipdb.set_trace()
    return str(test[state])

