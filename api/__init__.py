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
    
    with app.app_context():
        # Import routes
        from . import users, b_locals
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        # Jobs
        from .utils.scheduler import start_jobs
        #start_jobs()

        return app