from flask import Flask, render_template, request, url_for, redirect, session
# from app.routes import Instituicao
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import pymongo


app = Flask(__name__)
# app.config.from_object(Config)
# add secret key ?? 
# app.secret_key = "testing" || or use 'os.random(24)'
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://donatAdmin:p4KQ4EmLoLBm83ga@donat-cluster.jd6pl.mongodb.net/Donat-Cluster?retryWrites=true&w=majority")
db = client.Donat
users = db.User
institutions = db.Instituicao

print('test', users.find_one())


if __name__ == "__main__":
  app.run(debug=True)

# db = client.get_database('')
# records = db.register


db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
from app import routes