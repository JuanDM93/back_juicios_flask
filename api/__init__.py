from flask import Flask
from flask_cors import CORS

"""Initialize Flask app."""
def create_app():
    """Construct the core application."""
    app = Flask(
        __name__,
        instance_relative_config=False,
    )
    app.config.from_object('config.Config')

    # CORS
    CORS(app)

    # JWT & BCRYPT
    from .utils.auth import jwt, bcrypt
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # DB
    from .db import db
    db.init_app(app)
    
    # Jobs
    from .utils.scheduler import start_jobs
    #start_jobs(app)

    # Mail
    from .utils.mail.service import mail
    mail.init_app(app)

    with app.app_context():
        # Import routes
        from . import (
            admin, users,
            b_locals,)
        
        app.register_blueprint(admin.bp)
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        return app