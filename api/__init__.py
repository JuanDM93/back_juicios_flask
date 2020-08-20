from flask import Flask

"""Initialize Flask app."""
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # CORS
    from flask_cors import CORS
    #CORS(app, resources={r"*": {"origins": "*"}})

    with app.app_context():
        # Mail
        from flask_mail import Mail
        my_mail = Mail()
        
        # Import routes
        from . import users, b_locals
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        return app