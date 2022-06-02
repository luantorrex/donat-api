from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from flask_cors import CORS
from os import environ
from resources.errors import errors
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
CORS(app, supports_credentials=True)

if environ.get('PROD_DATABASE_URI'):
  app.config.from_object('config.ProdConfig')
elif environ.get('DEV_DATABASE_URI'):
  app.config.from_object('config.DevConfig')
else:
  app.config.from_object('config.TestConfig')

mail = Mail(app)
from controller.routes import initialize_routes

api = Api(app, errors=errors)


initialize_db(app)
initialize_routes(api)
jwt = JWTManager(app)

if __name__ == "__main__":
  app.run()