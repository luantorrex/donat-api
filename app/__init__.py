from flask import Flask, render_template, request, url_for, redirect, session
from config import Config
import pymongo
from app.models import User
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
  'host': 'mongodb+srv://donatAdmin:p4KQ4EmLoLBm83ga@donat-cluster.jd6pl.mongodb.net/Donat?retryWrites=true&w=majority'
}
db = MongoEngine()
db.init_app(app)

# app.config.from_object(Config)
# add secret key ?? 
# app.secret_key = "testing" || or use 'os.random(24)'
# app.secret_key = "testing"
# client = pymongo.MongoClient("mongodb+srv://donatAdmin:p4KQ4EmLoLBm83ga@donat-cluster.jd6pl.mongodb.net/Donat-Cluster?retryWrites=true&w=majority")
# users = db.User
print(User.objects())
# institutions = db.Instituicao

if __name__ == "__main__":
  app.run(debug=True)

from app import routes