# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # the issue is here
    # General configuration settings

    # use SECRET_KEY only for local dev testing and usage
    # SECRET_KEY = os.getenv("SECRET_KEY")
    if os.getenv('FLASK_ENV') == 'testing':
        # uncomment for local dev | comment for hosting
        # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY')}@localhost/dealership_testing"

        # comment for local dev
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:DHUvhsiNUNQMwrfUIqNCsVKWPebQBevT@roundhouse.proxy.rlwy.net:59865/dealership_testing"
    else:
        # uncomment for local dev | comment for hosting
        # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('SECRET_KEY')}@localhost/dealership_backend"

        # comment for local dev | uncomment for hosting
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:aGGeAzhlGdyhqpkesCDkjgcyKXHYXEuK@viaduct.proxy.rlwy.net:20836/dealership_backend"
    os.environ['FLASK_ENV'] = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
