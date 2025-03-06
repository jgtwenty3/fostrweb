from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from datetime import datetime
from config import db
from enums import RoleEnum, StatesEnum, SexEnum, AnimalStatusEnum
from sqlalchemy_serializer import SerializerMixin

bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(25), unique=True)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

    # Relationships
    owned_shelter = db.relationship('Shelter', back_populates='owner', foreign_keys='Shelter.owner_id')  

    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role.name if self.role else None,
        }

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Shelter(db.Model, SerializerMixin):
    __tablename__ = "shelters"
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(25), unique=True)
    street_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Enum(StatesEnum), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    about = db.Column(db.String(500))
    
    # Foreign Key
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))  

    # Relationships
    owner = db.relationship('User', back_populates='owned_shelter', foreign_keys=[owner_id])  
    animals = db.relationship('Animal', back_populates='shelter')  # Shelter owns many animals

    serialize_rules = ('-owner.password_hash',)  # Exclude owner password when serializing shelter
    def to_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state.name,
            'zipcode': self.zipcode,
            'about': self.about,
            # Exclude owner details to avoid recursion
        }
        return result

class Animal(db.Model, SerializerMixin):
    __tablename__ = "animals"
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    rescue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rescue_info = db.Column(db.String(500))
    species = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Enum(SexEnum), nullable=False)
    weight = db.Column(db.String())
    description = db.Column(db.String(500))
    special_needs = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(AnimalStatusEnum), nullable=False)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.id'))  # Foreign key for shelter
   
    
    shelter = db.relationship('Shelter', back_populates='animals')  # Shelter owns many animals
    medical_records = db.relationship('MedicalRecord', back_populates='animal')  # Animal has many medical records
    messages = db.relationship('Message', back_populates='animal')  # Messages linked to animals (optional)
   
    def to_dict(self):
            # Convert Enum fields to their string values
            animal_dict = {
                'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'name': self.name,
                'rescue_date': self.rescue_date,
                'rescue_info': self.rescue_info,
                'species': self.species,
                'breed': self.breed,
                'age': self.age,
                'sex': self.sex.value if self.sex else None,  # Convert Enum to string
                'weight': self.weight,
                'description': self.description,
                'special_needs': self.special_needs,
                'status': self.status.value if self.status else None,  # Convert Enum to string
                'shelter_id': self.shelter_id,
            }
            return animal_dict
   

class MedicalRecord(db.Model, SerializerMixin):
    __tablename__ = "medical_records"
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))  # Foreign key for the animal
    diagnosis = db.Column(db.String(500), nullable=False)
    treatment = db.Column(db.String(500))
    allergies = db.Column(db.String())
    existing_conditions = db.Column(db.String(1000))
    rabies_shot = db.Column(db.Boolean, default = False)
    rabies_date = db.Column(db.DateTime, default=datetime.utcnow)
    snap_shot = db.Column(db.Boolean, default = False)
    snap_date = db.Column(db.DateTime, default=datetime.utcnow)
    dhpp_shot = db.Column(db.Boolean, default = False)
    dhpp_date = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_record = db.Column(db.DateTime, default=datetime.utcnow)
    
    animal = db.relationship('Animal', back_populates='medical_records')  # Each medical record is linked to an animal


class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key for sender
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key for recipient
    content = db.Column(db.Text, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=True)  # Optional foreign key for animal-related messages
    
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='received_messages')
    animal = db.relationship('Animal', back_populates='messages')

# Reverse relationships for User and Animal

User.sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
User.received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient')
Animal.messages = db.relationship('Message', back_populates='animal')
