# Flask
from flask import Flask
app = Flask(__name__)
app.config.from_object('config.Config')

# Import routes
from api import users, b_locals
app.register_blueprint(users.bp)
app.register_blueprint(b_locals.bp)

# CORS
from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)