# DB
from flask_mysqldb import MySQL
db = MySQL()
#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

# JWT
from flask_jwt_extended import JWTManager
jwt  = JWTManager()

# Cors
from flask_cors import CORS
CORS()

# Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# Mail
from flask_mail import Mail
mail = Mail() 


from flask import Flask

"""Initialize Flask app."""
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # Import routes
        from . import users, b_locals

        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        return app