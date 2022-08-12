import os
from dotenv import load_dotenv


SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Enable debug mode.
DEBUG = True

# Connect to the database
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{PASSWORD}@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False 