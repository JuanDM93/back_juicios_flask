from flask import current_app

# JWT & Bcrypt
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

def init_auth():
    jwt = JWTManager(current_app)
    bcrypt = Bcrypt(current_app)
    return jwt, bcrypt
