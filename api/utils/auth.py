# JWT & Bcrypt
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


def init_auth():
    return JWTManager(), Bcrypt()
