# JWT & Bcrypt
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


jwt = JWTManager()
bcrypt = Bcrypt()
