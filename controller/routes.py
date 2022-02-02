# from app import app 
# from dataConsumer import consumingDataPerDate as dpd
# from initials import initialsToState
# from news import callGoogle
# from datetime import date, timedelta
# import json
# from flask_restful import Api, Resource, reqparse
# from flask import request, jsonify, session
# from app.database.models import Instituicao
# from werkzeug.security import generate_password_hash, check
# from helper

# defaultDay = date.today()-timedelta(days=1)
# defaultDay = defaultDay.strftime("%m-%d-%Y")

from controller.auth.auth import Login, Logout, Register
from controller.institution import InstituicaoById, Institution
from controller.user import getLoggedUser


def initialize_routes(api):    
    api.add_resource(Institution, "/api/instituicao")
    api.add_resource(InstituicaoById, "/api/instituicao/<string:id>")
    
    api.add_resource(Login, "/api/login")
    api.add_resource(Register, "/api/register")
    api.add_resource(Logout, "/api/logout")
    
    api.add_resource(getLoggedUser, "/api/get_logged_user")

# @app.route("/api/news")
# @app.route("/api/news/<string:state>")
# def showNews(state="Brasil"):
#     state = state.upper()
#     if state not in initialsToState:
#         state = "Brasil"
#     else:
#         state = initialsToState[state]
#     return str(callGoogle(state))