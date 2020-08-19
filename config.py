"""Flask configuration variables."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    #SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
    MYSQL_DB = 'juicios'
    MYSQL_CURSORCLASS = 'DictCursor'

    # JWT
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = False #60 * 60

    # Mail 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'yourId@gmail.com'
    MAIL_PASSWORD = '*****'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
