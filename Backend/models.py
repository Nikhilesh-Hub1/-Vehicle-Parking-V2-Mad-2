from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    reservations = db.relationship('Reservation', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
    

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=10.0)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete-orphan')

    def to_dict(self):
        available_spots = len([s for s in self.spots if s.status == 'A'])
        return {
            "id": self.id,
            "prime_location_name": self.prime_location_name,
            "price": self.price_per_hour,
            "address": self.address,
            "pin_code": self.pin_code,
            "number_of_spots": self.number_of_spots,
            "available_spots": available_spots
        }

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # A = Available, O = Occupied
    reservations = db.relationship('Reservation', backref='spot', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ParkingSpot {self.id} in Lot {self.lot_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "lot_id": self.lot_id,
            "status": self.status
        }



class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "spot_id": self.spot_id,
            "user_id": self.user_id,
            "parking_timestamp": self.parking_timestamp.isoformat(),
            "leaving_timestamp": self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            "parking_cost": self.parking_cost
        }
































with app.app_context():
    db.create_all()


    admin = User.query.filter_by(email = 'admin@gmail.com').first()
    if not admin :
        admin = User(name='admin',email = 'admin@gmail.com',password = 'admin', role = 'admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created with email:", "admin@gmail.com", "and password:", "admin")
