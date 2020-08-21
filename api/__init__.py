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
    
    # DB
    from .db import db
    db.init_app(app)
    
    # Jobs
    from .utils.scheduler import start_jobs
    #start_jobs(app)

    # Mail
    from .utils.mail import mail
    mail.init_app(app)

    with app.app_context():
        # Import routes
        from . import users, b_locals, admin
        
        app.register_blueprint(users.bp)
        app.register_blueprint(b_locals.bp)

        app.register_blueprint(admin.bp)

        # test mail
        from .utils.mail import sendMail
        m_to = ['ricaror@hotmail.com',]
        #result = sendMail(m_to)

        return app