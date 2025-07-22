from flask_restful import Api, Resource
from flask import Flask, render_template, request, jsonify
from models import db, User, ParkingLot, ParkingSpot, Reservation
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity,verify_jwt_in_request
from functools import wraps
from datetime import datetime,timedelta
from app import app







def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request() 
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'admin':
            return {"message": "Access forbidden: Admins only"}, 403
        return fn(*args, **kwargs)

    return wrapper




class Users(Resource):
    @jwt_required()
    @admin_required
    def get(self, user_id=None):
        current_user = User.query.get(get_jwt_identity())
          
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
    
class Register(Resource):
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
        
    

class Login(Resource):
    def post(self):
      
        try:
            email = request.json.get('email')
            password = request.json.get('password')
            user = User.query.filter_by(email=email, password=password).first()
            if user:
                access_token = create_access_token(identity=user.id,expires_delta=timedelta(hours=24))
                user = User.query.get(user.id)
                return {"message": "Login successful", "access_token": access_token, "user": user.to_dict()}, 200
            
            else:
                return {"message": "Invalid credentials"}, 401
        except Exception as e:
            print(f"Error: {e}")
            return {"message": "Error occurred during login", "error": str(e)}, 500
        
        
    
#---------------------------------------PARKING LOT CONTROLLERS---------------------------------------

class ParkingLotsAPI(Resource):
    @jwt_required()
    
    def get(self, lot_id=None):
        if lot_id:
            lot = ParkingLot.query.get(lot_id)
            if not lot:
                return {"message": "Parking Lot not found"}, 404
            return {"message": "Parking Lot fetched successfully", "lot": lot.to_dict()}, 200
        else:
            lots = ParkingLot.query.all()
            return jsonify({'message': 'Parking Lots fetched successfully', 'lots': [lot.to_dict() for lot in lots]})
    @admin_required
    def post(self):
        try:
            data = request.get_json()
            new_lot = ParkingLot(
                prime_location_name=data['prime_location_name'],
                price_per_hour=data['price'],
                address=data['address'],
                pin_code=data['pin_code'],
                number_of_spots=data['number_of_spots']
            )
            db.session.add(new_lot)
            db.session.commit()
            for _ in range(new_lot.number_of_spots):
                spot = ParkingSpot(status='A', lot_id=new_lot.id)
                db.session.add(spot)
                db.session.commit()
            return {"message": "Parking Lot created successfully", "lot": new_lot.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during creation", "error": str(e)}, 500
        finally:
            db.session.close()

    @admin_required
    def put(self, lot_id):
        try:
            lot = ParkingLot.query.get(lot_id)
            if not lot:
                return {"message": "Parking Lot not found"}, 404

            data = request.get_json()

            # Update lot fields
            lot.prime_location_name = data['prime_location_name']
            lot.price_per_hour = data['price_per_hour']
            lot.address = data['address']
            lot.pin_code = data['pin_code']

            new_spot_count = data['number_of_spots']
            current_spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
            current_count = len(current_spots)

            if new_spot_count > current_count:
                # Add new spots
                for _ in range(new_spot_count - current_count):
                    new_spot = ParkingSpot(status='A', lot_id=lot.id)
                    db.session.add(new_spot)

            elif new_spot_count < current_count:
                # Try removing only available spots
                removable_spots = [spot for spot in current_spots if spot.status == 'A']
                spots_to_remove = current_count - new_spot_count

                if len(removable_spots) < spots_to_remove:
                    return {
                        "message": "Cannot remove occupied spots. Free up spots first."
                    }, 400

                for spot in removable_spots[:spots_to_remove]:
                    db.session.delete(spot)

            # Update the spot count in the lot
            lot.number_of_spots = new_spot_count

            db.session.commit()
            return {"message": "Parking Lot updated successfully", "lot": lot.to_dict()}, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during update", "error": str(e)}, 500

        finally:
            db.session.close()


    @admin_required
    def delete(self, lot_id):
        try:
            lot = ParkingLot.query.get(lot_id)
            if not lot:
                return {"message": "Parking Lot not found"}, 404
            
            db.session.delete(lot)
            db.session.commit()
            return {"message": "Parking Lot deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during deletion", "error": str(e)}, 500
        finally:
            db.session.close()


#---------------------------------------PARKING SPOT CONTROLLERS---------------------------------------

class ParkingSpotsAPI(Resource):
    @jwt_required()
    def get(self, spot_id=None):
        if spot_id:
            spot = ParkingSpot.query.get(spot_id)
            if not spot:
                return {"message": "Parking Spot not found"}, 404
            return {"message": "Parking Spot fetched successfully", "spot": spot.to_dict()}, 200
        else:
            spots = ParkingSpot.query.all()
            return jsonify({'message': 'Parking Spots fetched successfully', 'spots': [spot.to_dict() for spot in spots]})
    
    @admin_required
    def post(self):
        try:
            data = request.get_json()
            new_spot = ParkingSpot(
                lot_id=data['lot_id'],
                status=data.get('status', 'A')  
            )
            lot = ParkingLot.query.get(data['lot_id'])
            if not lot:
                return {"message": "Parking Lot not found"}, 404
            if len(lot.spots) >= lot.number_of_spots:
                return {
                "message": "Cannot add more spots. Lot is full",
                "available_spots": lot.number_of_spots - len(lot.spots)
                }, 400
            db.session.add(new_spot)
            db.session.commit()
            return {"message": "Parking Spot created successfully", "spot": new_spot.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during creation", "error": str(e)}, 500
        finally:
            db.session.close()

    @admin_required
    def put(self, spot_id):
        try:
            spot = ParkingSpot.query.get(spot_id)
            if not spot:
                return {"message": "Parking Spot not found"}, 404

            data = request.get_json()
            spot.lot_id = data['lot_id']
            spot.status = data.get('status', spot.status)  
            db.session.commit()
            return {"message": "Parking Spot updated successfully", "spot": spot.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during update", "error": str(e)}, 500
        finally:
            db.session.close()
    @admin_required
    def delete(self, spot_id):
        try:
            spot = ParkingSpot.query.get(spot_id)
            if not spot:
                return {"message": "Parking Spot not found"}, 404
            
            db.session.delete(spot)
            db.session.commit()
            return {"message": "Parking Spot deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during deletion", "error": str(e)}, 500
        finally:
            db.session.close()

#---------------------------------------RESERVATION CONTROLLERS---------------------------------------

class ReservationAPI(Resource):
    @jwt_required()
    def get(self, reservation_id=None):
        def enrich(reservation):
            data = reservation.to_dict()

            spot = ParkingSpot.query.get(reservation.spot_id)
            lot = ParkingLot.query.get(spot.lot_id) if spot else None
            rate_per_hour = lot.price_per_hour if lot else 10.0

            # Use current time if reservation is still ongoing
            end_time = reservation.leaving_timestamp or datetime.utcnow()

            duration_seconds = (end_time - reservation.parking_timestamp).total_seconds()
            duration_hours = duration_seconds / 3600
            duration_minutes = int(duration_seconds // 60)

            hours = duration_minutes // 60
            minutes = duration_minutes % 60

            human_duration = []
            if hours:
                human_duration.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes:
                human_duration.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            readable = " ".join(human_duration) if human_duration else "Less than a minute"

            data.update({
                "duration_hours": round(duration_hours, 2),
                "human_readable_duration": readable,
                "price_per_hour": rate_per_hour,
                "parking_cost": reservation.parking_cost,
                "lot_name": lot.prime_location_name if lot else "Unknown Lot",
                "lot_id": lot.id if lot else None,
                "spot_id": spot.id if spot else None,
                "status_message": "Reservation ended" if reservation.leaving_timestamp else "Reservation ongoing"
            })

            return data

        if reservation_id:
            reservation = Reservation.query.get(reservation_id)
            if not reservation:
                return {"message": "Reservation not found"}, 404

            return {
                "message": "Reservation fetched successfully",
                "reservation": enrich(reservation)
            }, 200

        else:
            reservations = Reservation.query.all()
            enriched_data = [enrich(res) for res in reservations]
            return jsonify({
                'message': 'Reservations fetched successfully',
                'reservations': enriched_data
            })


    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            spot = ParkingSpot.query.get(data['spot_id'])
            if not spot:
                return {"message": "Parking Spot not found"}, 404

            if spot.status != 'A':
                return {"message": "Parking Spot is not available"}, 400

            reservation = Reservation(
                spot_id=spot.id,
                user_id=user.id,
                parking_timestamp=datetime.utcnow()
            )

            spot.status = 'O'
            db.session.add(reservation)
            db.session.commit()

            return {"message": "Reservation created successfully", "reservation": reservation.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during reservation", "error": str(e)}, 500
        finally:
            db.session.close()
    @admin_required
    def delete(self, reservation_id):
        try:
            reservation = Reservation.query.get(reservation_id)
            if not reservation:
                return {"message": "Reservation not found"}, 404
            
            spot = ParkingSpot.query.get(reservation.spot_id)
            if not spot:
                return {"message": "Parking Spot not found"}, 404
            
            spot.status = 'A'  
            db.session.delete(reservation)
            db.session.commit()
            return {"message": "Reservation deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during deletion", "error": str(e)}, 500
        finally:
            db.session.close()

class ReservationEndAIP(Resource):
    @jwt_required()
    def put(self, reservation_id):
        try:
            reservation = Reservation.query.get(reservation_id)
            if not reservation:
                return {"message": "Reservation not found"}, 404
            if reservation.leaving_timestamp:
                return {"message": "Reservation already ended"}, 400

            reservation.leaving_timestamp = datetime.utcnow()
            reservation.parking_cost = self.calculate_parking_cost(reservation)

            # Mark the spot as available
            spot = ParkingSpot.query.get(reservation.spot_id)
            if spot:
                spot.status = 'A'

            db.session.commit()

            rate_per_hour = ParkingLot.query.get(spot.lot_id).price_per_hour or 10.0
            duration_seconds = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds()
            duration_hours = duration_seconds / 3600
            
            return {
                    "message": "Reservation ended successfully",
                    "reservation": reservation.to_dict(),
                    "duration_hours": round(duration_hours, 2),
                    "price_per_hour": rate_per_hour
                    }, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return {"message": "Error occurred during ending reservation", "error": str(e)}, 500

        finally:
            db.session.close()

    def calculate_parking_cost(self, reservation):
        if not reservation.leaving_timestamp:
            return 0.0

        # Get the parking spot
        spot = ParkingSpot.query.get(reservation.spot_id)
        if not spot:
            return 0.0

        # Get the parking lot that owns the spot
        lot = ParkingLot.query.get(spot.lot_id)
        if not lot:
            return 0.0

        rate_per_hour = lot.price_per_hour or 10.0  # fallback to 10 if not set

        # Time calculations — exact duration in hours
        duration_seconds = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds()
        duration_hours = duration_seconds / 3600

        # Calculate cost
        cost = duration_hours * rate_per_hour

        reservation.parking_cost = round(cost, 2)
        db.session.commit()
        return reservation.parking_cost


#---------------------------------------APP SETUP---------------------------------------

        

#---------------------------------------API SETUP---------------------------------------
api = Api(app)

api.add_resource(Authenticate, '/api/auth')
api.add_resource(Users, '/api/users', '/api/users/<int:user_id>')
api.add_resource(Register, '/api/register') 
api.add_resource(Login, '/api/login')

#parking lot and spot resources
api.add_resource(ParkingLotsAPI, '/api/parking_lots', '/api/parking_lots/<int:lot_id>')
api.add_resource(ParkingSpotsAPI, '/api/parking_spots', '/api/parking_spots/<int:spot_id>')
api.add_resource(ReservationAPI, '/api/reservations', '/api/reservations/<int:reservation_id>')
api.add_resource(ReservationEndAIP, '/api/reservations/end/<int:reservation_id>')


   