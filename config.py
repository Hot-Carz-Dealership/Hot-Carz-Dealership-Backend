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
        # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY_3')}@localhost/dealership_testing"
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY_2')}@roundhouse.proxy.rlwy.net:59865/dealership_testing"

    else:
        # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY_3')}@localhost/dealership_backend"
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY_1')}@viaduct.proxy.rlwy.net:20836/dealership_backend"

    os.environ['FLASK_ENV'] = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
