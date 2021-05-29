from app import app
from app.dataConsumer import consumingData


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/data')
@app.route('/data/test')
def showData():
    test = consumingData()
    #import ipdb; ipdb.set_trace()
    return str(test)

