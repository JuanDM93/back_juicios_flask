from flask import Flask

"""Initialize Flask app."""
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    # CORS
    from flask_cors import CORS
    CORS(
        app,
        #supports_credentials=True,
        send_wildcard=True,
        )

    with app.app_context():
        # Import routes
        from . import users, b_locals
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        return app