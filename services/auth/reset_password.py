import datetime

from flask_restful import Resource

from database.models import User
from flask import render_template, request
from flask_jwt_extended import create_access_token, decode_token
from werkzeug.security import generate_password_hash
from resources.errors import InternalServerError, SchemaValidationError
from resources.mail_service import send_email


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                raise SchemaValidationError
            
            user = User.objects.get(email = email)
            if not user:
                raise "Email does not exist!"
            
            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user.pk), expires_delta=expires)
            
            return send_email('[Donat] Reset Your Password',
                              sender='support@donat.com',
                              recipients=[user.email],
                              text_body=render_template('email/reset_password.txt',
                                                        url=url + reset_token),
                              html_body=render_template('email/reset_password.html',
                                                        url="http://localhost:4200/home" + reset_token))
        except SchemaValidationError:
            raise SchemaValidationError
        except Exception as e:
            raise e
        
class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')

            if not reset_token or not password:
                raise SchemaValidationError

            user_id = decode_token(reset_token)['sub']

            user = User.objects.get(pk=user_id)

            user.modify(password=generate_password_hash(password))
            user.save()

            return send_email('[Donat] Password reset successful',
                              sender='support@donat.com',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

        except SchemaValidationError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError
