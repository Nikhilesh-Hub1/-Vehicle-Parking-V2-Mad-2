from flask_restful import Api, Resource
from flask import Flask, render_template, request, jsonify
from models import db, User

class Users(Resource):

    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return {"message": "User fetched successfully", "user": user.to_dict()}, 200
        else:
            users = User.query.all()
            return jsonify({'message': 'Users fetched successfully', 'users': [user.to_dict() for user in users]})
    
    def put(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            
            data = request.get_json()
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)
            db.session.commit()
            return {"message": "User updated successfully", "user": user.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during update", "error": str(e)}, 500
        finally:
            db.session.close()

    def delete(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during deletion", "error": str(e)}, 500
        finally:
            db.session.close()
    

class Authenticate(Resource):
    def post(self):
        try:
            email = request.json.get('email')
            password = request.json.get('password')
            user = User.query.filter_by(email=email, password=password).first()
            if user:
                return {"message": "Authentication successful", "user": user.to_dict()}, 200
            else:
                return {"message": "Invalid credentials"}, 401
        except Exception as e:
            print(f"Error: {e}")
            return {"message": "Error occurred during authentication", "error": str(e)}, 500
    
class register(Resource):
    def post(self):
        try:
            email = request.json.get('email')
            if User.query.filter_by(email=email).first():
                return {"message": "Email already exists"}, 400
            data = request.get_json()
            new_user = User(name=data['name'], email=data['email'], password=data['password'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successfully", "user": new_user.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during registration", "error": str(e)}, 500
        finally:
            db.session.close()
        
    


    def put(self):
        return jsonify({"message": "PUT Registration successful"})
    def delete(self):
        return jsonify({"message": "DELETE Registration successful"}) 
