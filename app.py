from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from controller.routes import initialize_routes
from flask_cors import CORS
from os import environ
from helper.errors import errors

app = Flask(__name__)
CORS(app)

if environ.get('PROD_DATABASE_URI'):
  app.config.from_object('config.ProdConfig')
else:
  app.config.from_object('config.DevConfig')

api = Api(app, errors=errors)

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
  app.run()