"""Flask configuration variables."""
from os import environ, path


basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    # SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    # MYSQL_HOST = 'db'        # Docker
    MYSQL_HOST = 'localhost'       # Local
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'juicios'
    MYSQL_CURSORCLASS = 'DictCursor'

    # JWT
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = False    # 60 * 60

    # SCHEDULER
    SCHEDULER_API_ENABLED = True

    # TIKA
    # TIKA_CLIENT_ONLY = True
    # TIKA_SERVER_ENDPOINT = 'http://tika:9998/tika'

    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_USERNAME')
