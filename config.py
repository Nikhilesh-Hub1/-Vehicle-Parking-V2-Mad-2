from dotenv import load_dotenv 
from os import getenv
from flask_jwt_extended import JWTManager


from app import app
import os
load_dotenv()

#database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#jwt config
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  
app.config['JWT_VERIFY_SUB'] = False  
jwt = JWTManager(app)
