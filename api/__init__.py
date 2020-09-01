"""Initialize Flask app."""
from flask import Flask
from flask_cors import CORS


def create_app():
    """Construct the core application."""
    app = Flask(
        __name__,
        instance_relative_config=False,
    )
    app.config.from_object('config.Config')

    with app.app_context():
        # CORS
        CORS(app)

        # JWT & BCRYPT
        from .utils.auth import init_auth
        init_auth(app)

        # DB
        from .utils.db import db
        db.init_app(app)

        # Mail
        from .utils.mail.service import mail
        mail.init_app(app)
        app.extensions['mail'].debug = 0    # No logging

        # Jobs
        from .utils.scheduler import start_jobs
        start_jobs(app)

        # Import routes
        from .routes import (
            admin, users,
            b_locals, b_federals)

        app.register_blueprint(admin.bp)
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)
        app.register_blueprint(b_federals.bp)

        return app
