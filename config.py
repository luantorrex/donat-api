"""Flask configuration."""
import datetime
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET_KEY =  environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
    JWT_SESSION_COOKIE = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = "465"
    MAIL_USERNAME = "dd413582228@gmail.com"
    MAIL_PASSWORD = environ.get('EMAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {'host': environ.get('PROD_DATABASE_URI')}
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_COOKIE_SECURE = True ## sempre deixar true em prod
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_CSRF_PROTECT = True


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    MONGODB_SETTINGS = {'host': environ.get('DEV_DATABASE_URI')}
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_SESSION_COOKIE = True
    
    
class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {'host': 'mongomock://localhost'}
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
