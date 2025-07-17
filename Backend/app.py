from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from models import db, User
db.init_app(app)



from controllers import Api, Authenticate, Users, register
api = Api(app)

api.add_resource(Authenticate, '/api/auth')
api.add_resource(Users, '/api/users', '/api/users/<int:user_id>')
api.add_resource(register, '/api/register') 







if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)