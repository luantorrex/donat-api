from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)

app.secret_key = "testing"
app.config['MONGODB_SETTINGS'] = {
  'host': 'mongodb+srv://donatAdmin:p4KQ4EmLoLBm83ga@donat-cluster.jd6pl.mongodb.net/Donat?retryWrites=true&w=majority'
}
db = MongoEngine()
db.init_app(app)

if __name__ == "__main__":
  app.run()

from app import routes