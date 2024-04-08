# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config  # Import the configuration

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/docs.yml'  # Our API url (can of course be a local resource)

app = Flask(__name__)

db_name = 'dealership_backend'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/' + db_name

# Load the configuration
app.config.from_object(Config)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, supports_credentials=True)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Set up database migration
migrate = Migrate(app, db)

# session app confic code for flask
app.config['SECRET_KEY'] = 'secret_key'  # sets the secret key for the Flask application for session cookies

# app.config['SESSION_TYPE'] = 'filesystem'  # configures the type of session storage to be used. In this case, it sets the session storage type to be stored on the filesystem
# basically this stores session data in the app in our file systems but idk if it works.

app.debug = True  # enables debugging in the flask app

from app import routes, models  # Import routes and models
