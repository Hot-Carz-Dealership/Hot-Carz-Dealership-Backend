# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # the issue is here
    # General configuration settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    if os.getenv('FLASK_ENV') == 'testing':
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY')}@localhost/dealership_testing"
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY')}@localhost/dealership_backend"

    os.environ['FLASK_ENV'] = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
