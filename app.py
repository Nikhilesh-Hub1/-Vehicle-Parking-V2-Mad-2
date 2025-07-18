from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token,jwt_manager

app = Flask(__name__)
CORS(app)

import config
import models




from controllers import Api, Authenticate, Users, register
api = Api(app)

api.add_resource(Authenticate, '/api/auth')
api.add_resource(Users, '/api/users', '/api/users/<int:user_id>')
api.add_resource(register, '/api/register') 








   