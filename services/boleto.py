import os
from flask import after_this_request, request, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from resources import billet_generator

    
class boleto(Resource):
    @jwt_required()
    def get(self):
        # remove_file will be executed after the creation of boleto pdf in assets.     
        @after_this_request
        def remove_file(response):
            os.remove("./assets/boleto.pdf")
            return response    
              
        billet = billet_generator.print_custom_data(request.args['institution'], request.args['user'], float(request.args['value']))
        billet.save("./assets/boleto.pdf")
        return send_from_directory("./assets", "boleto.pdf")
        
