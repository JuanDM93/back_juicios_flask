# JWT & Bcrypt
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


jwt = JWTManager()
bcrypt = Bcrypt()


def init_auth(app):
    jwt.init_app(app)
    bcrypt.init_app(app)