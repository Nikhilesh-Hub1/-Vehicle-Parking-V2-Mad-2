from flask import Flask
from flask_cors import CORS
from config import init_app
from extensions import db
from models import User  # Importing models after db is initialized

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Initialize config
    init_app(app)
    
    # Creating tables and admin user
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin = User(
                name='admin',
                email='admin@gmail.com',
                password='admin', 
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")

    return app

app = create_app()

from controllers import *

if __name__ == '__main__':
    app.run(debug=True)

