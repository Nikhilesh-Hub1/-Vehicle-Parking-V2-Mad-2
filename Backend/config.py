from dotenv import load_dotenv
import os
from extensions import db, jwt,cache

load_dotenv()

def init_app(app):
   
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_VERIFY_SUB'] = False

    #flask_caching configuration
    app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'simple')
    app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))

    # Initializing extensions
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

