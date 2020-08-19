"""Flask configuration variables."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    #SECRET_KEY = environ.get('SECRET_KEY')

    #export FLASK_APP=app_name False
    FLASK_APP = environ.get('FLASK_APP')
    #export FLASK_ENV=development False
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
    MYSQL_DB = 'juicios'
    MYSQL_CURSORCLASS = 'DictCursor'

    # General Config
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = False #60 * 60