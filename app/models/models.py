from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True, nullable=False)
    domicile_type = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), nullable=False)
    user_info = db.Column(db.String(2000))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User with {self.email} and {self.password}'

    def to_dictionary(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "image_url": self.image_url,
            "user_info": self.user_info,
        }

class Calendar(db.Model):
    __tablename__ = 'calendar'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location_id = db.Column(db.Integer,
        db.ForeignKey('locations.id'),
        nullable=False)
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)

    user = db.relationship('User', backref='calendar', lazy=True)
    # backref establishes parent.children AND children.parent relationship meaning...
    # if you add <User instance> to <Calendar instance> by <Calendar instance>.user = <User instance>
    # then you will be able to also call <User instance>.calendar
    # <User instance>.calendar equals a LIST, so if you want to key into <Calendar instance>...
    # you must index into it by <User instance>.calendar[0].start_date
    locations = db.relationship('Location', backref='location', lazy=True)


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    starting_address = db.Column(db.String(100), nullable=False)
    starting_city = db.Column(db.String(50), nullable=False)
    starting_state = db.Column(db.String(20), nullable=False)
    ending_address = db.Column(db.String(100), nullable=False)
    ending_city = db.Column(db.String(50), nullable=False)
    ending_state = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)

    user = db.relationship('User', backref='trip', lazy=True)


class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    electric_hookup = db.Column(db.Boolean)
    water_hookup = db.Column(db.Boolean)
    septic_hookup = db.Column(db.Boolean)
    assigned_parking = db.Column(db.Boolean)
    tow_vehicle_parking = db.Column(db.Boolean)
    trash_removal = db.Column(db.Boolean)
    water_front = db.Column(db.Boolean)
    pets_allowed = db.Column(db.Boolean)
    internet_access = db.Column(db.Boolean)


class Necessity(db.Model):
    __tablename__ = 'necessities'

    id = db.Column(db.Integer, primary_key=True)
    rv_compatible = db.Column(db.Boolean)
    generators_allowed = db.Column(db.Boolean)
    fires_allowed = db.Column(db.Boolean)
    max_days = db.Column(db.Integer)
    pad_type = db.Column(db.String(100))


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    gps_coords = db.Column(db.String(100), nullable=False)
    image_urls = db.Column(db.ARRAY(db.String(255)))
    # ARRAY types only supported in Postgres
    website = db.Column(db.String(255))
    description = db.Column(db.String(2000))
    host_notes = db.Column(db.String(2000))
    active = db.Column(db.Boolean, default=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    necessity_id = db.Column(db.Integer, db.ForeignKey('necessities.id'), nullable=False)

    amenity = db.relationship('Amenity', backref='location', lazy=True)
    user = db.relationship('User', backref='location', lazy=True)
    necessity = db.relationship('Necessity', backref='location', lazy=True)

    def __repr__(self):
        return f'<Location: {self.address} - {self.city} - {self.state} - {self.gps_coords} >'

    def to_dictionary(self):
        return {
            "id": self.id,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "gps_coords": self.gps_coords,
            "image_urls": self.image_urls,
            "website": self.website,
            "description": self.description,
            "host_notes": self.host_notes,
            "active": self.active,
            "host_first_name": self.user.first_name,
            "host_last_name": self.user.last_name,
            "host_info": self.user.user_info,
            "electric_hookup": self.amenity.electric_hookup,
            "water_hookup": self.amenity.water_hookup,
            "septic_hookup": self.amenity.septic_hookup,
            "assigned_parking": self.amenity.assigned_parking,
            "tow_vehicle_parking": self.amenity.tow_vehicle_parking,
            "trash_removal": self.amenity.trash_removal,
            "water_front": self.amenity.water_front,
            "pets_allowed": self.amenity.pets_allowed,
            "internet_access": self.amenity.internet_access,
            "rv_compatible": self.necessity.rv_compatible,
            "generators_allowed": self.necessity.generators_allowed,
            "fires_allowed": self.necessity.fires_allowed,
            "max_days": self.necessity.max_days,
            "pad_type": self.necessity.pad_type,
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    overall_rating = db.Column(db.Integer)
    noise = db.Column(db.Integer)
    safety = db.Column(db.Integer)
    cleanliness = db.Column(db.Integer)
    access = db.Column(db.Integer)
    site_quality = db.Column(db.Integer)
    comments = db.Column(db.String(2000))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    location_id = db.Column(db.Integer,
        db.ForeignKey('locations.id'),
        nullable=False)

    user = db.relationship('User', backref='review', lazy=True)
    location = db.relationship('Location', backref='review', lazy=True)
