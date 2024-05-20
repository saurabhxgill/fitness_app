# This is instance/config.py
import os

# Secret key for securing sessions
SECRET_KEY = os.urandom(24)  # Generates a random key

# Database configuration
SQLALCHEMY_DATABASE_URI = "sqlite:///calorie_tracker.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask application debugging
DEBUG = True
