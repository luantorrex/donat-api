from app import app
from app.dataConsumer import consumingData as cd

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/data')
def showData():
    cd()
    return ''