from extensions import db

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
    price_per_hour = db.Column(db.Float, nullable=False, server_default='10.0')
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete-orphan')


    def to_dict(self):
        available_spots = len([s for s in self.spots if s.status == 'A'])

        # Sort spots by ID 
        sorted_spots = sorted(self.spots, key=lambda s: s.id)

        # Creating 2D grid (3 columns per row for example)
        grid = []
        row = []
        for i, spot in enumerate(sorted_spots):
            row.append({
                "id": spot.id,
                "lot_id": spot.lot_id,
                "status": spot.status            
            })
            if (i + 1) % 5 == 0:  # Adjust this number for different row sizes
                grid.append(row)
                row = []
        if row:  # Add any remaining row
            grid.append(row)


        return {
            "id": self.id,
            "prime_location_name": self.prime_location_name,
            "price_per_hour": self.price_per_hour,
            "address": self.address,
            "pin_code": self.pin_code,
            "number_of_spots": self.number_of_spots,
            "available_spots": available_spots,
            "grid": grid
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
    vehicle_number = db.Column(db.String(20))


    def to_dict(self):
        return {
            "id": self.id,
            "spot_id": self.spot_id,
            "user_id": self.user_id,
            "parking_timestamp": self.parking_timestamp.isoformat(),
            "leaving_timestamp": self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            "parking_cost": self.parking_cost,
            "vehicle_number": self.vehicle_number
            
        }









