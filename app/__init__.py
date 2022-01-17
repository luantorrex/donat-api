from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine


app = Flask(__name__)
CORS(app)
app.config.from_object('config.DevConfig')
db = MongoEngine()
db.init_app(app)

if __name__ == "__main__":
  app.run()

from app import routes