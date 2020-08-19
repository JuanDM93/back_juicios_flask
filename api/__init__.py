from flask import Flask

"""Initialize Flask app."""
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    from flask_cors import CORS
    CORS(app)
        
    #from flask_sqlalchemy import SQLAlchemy
    #db = SQLAlchemy()

    with app.app_context():

        # JWT
        from flask_jwt_extended import JWTManager
        jwt  = JWTManager()

        # Bcrypt
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        
        # DB
        from flask_mysqldb import MySQL
        from .self_db import db_connect
        my_db = MySQL()
        
        # Import routes
        from . import users, b_locals
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        return app