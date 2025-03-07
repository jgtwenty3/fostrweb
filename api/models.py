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
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.id'))  
    
    shelter = db.relationship('Shelter', back_populates='workers')  
    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    likes = db.relationship('Like', back_populates='user')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient')
   
    
    
    serialize_rules = ('-password_hash', '-shelter_id')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role.name if self.role else None,
            'shelter': self.shelter.name if self.shelter else None,
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
    
    workers = db.relationship('User', backref='shelters')
    animals = db.relationship('Animal', back_populates='shelter')
    
    serialize_rules = ('-worker_id') 
    
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
            'workers': [worker.to_dict() for worker in self.workers],
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
   
    
    shelter = db.relationship('Shelter', back_populates='animals')
    medical_records = db.relationship('MedicalRecord', back_populates='animal')
    posts = db.relationship('Post', back_populates = "animal")
    
    serialize_rules = ('-shelter.id')  
    
    def to_dict(self):
        animal_dict = {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,  # Format datetime if available
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,  # Format datetime if available
            'name': self.name,
            'rescue_date': self.rescue_date.isoformat() if self.rescue_date else None,  # Format rescue date if available
            'rescue_info': self.rescue_info,  # Assuming rescue_info is a field
            'species': self.species,
            'breed': self.breed,
            'age': self.age,
            'sex': self.sex.value if self.sex else None,  # Convert Enum to string
            'weight': self.weight,
            'description': self.description,
            'special_needs': self.special_needs,
            'status': self.status.value if self.status else None,  # Convert Enum to string
            'shelter_name': self.shelter.name if self.shelter else None,  # Get shelter name
            'location': f"{self.shelter.city}, {self.shelter.state.value}" if self.shelter else None,  # Get shelter city and state
            'medical_records': [record.to_dict() for record in self.medical_records],  # Serialize medical records if any
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
    
    serialize_rules = ('-animal_id',)

    def to_dict(self):
        return {
        "id": self.id,
        "animal_id": self.animal_id,
        "diagnosis": self.diagnosis,
        "treatment": self.treatment,
        "allergies": self.allergies,
        "existing_conditions": self.existing_conditions,
        "rabies_shot": self.rabies_shot,
        "rabies_date": self.rabies_date.isoformat() if self.rabies_date else None,
        "snap_shot": self.snap_shot,
        "snap_date": self.snap_date.isoformat() if self.snap_date else None,
        "dhpp_shot": self.dhpp_shot,
        "dhpp_date": self.dhpp_date.isoformat() if self.dhpp_date else None,
        "date_of_record": self.date_of_record.isoformat() if self.date_of_record else None
        }


class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key for sender
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key for recipient
    content = db.Column(db.Text, nullable=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='received_messages')

# Reverse relationships for User and Animal

User.sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
User.received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient')


class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for user
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=True)  
    caption = db.Column(db.String(500), nullable=False)  # Caption for the post
    image_url = db.Column(db.String(500))  # URL for the image or video
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='posts')  # Each post is associated with a user
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')  # Comments on the post
    likes = db.relationship('Like', back_populates='post', cascade='all, delete-orphan')  # Likes on the post
    animal = db.relationship('Animal', back_populates="posts")

    
    serialize_rules = ('-user_id','-animal.posts')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'animal': self.animal.to_dict() if self.animal else None,
            'caption': self.caption,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user': self.user.to_dict(),  # Include user details for the post
            'comments': [comment.to_dict() for comment in self.comments],  # Serialize comments
            'likes_count': len(self.likes),  # Show the count of likes
        }
    

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for user
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # Foreign key for post
    content = db.Column(db.Text, nullable=False)  # The comment content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
    
    serialize_rules = ('-post_id', '-user_id')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'user': self.user.to_dict(),  # Include user details in comment
        }

class Like(db.Model, SerializerMixin):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for user
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # Foreign key for post
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')
    
    serialize_rules = ('-user_id', 'post_id')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'created_at': self.created_at.isoformat(),
            'user': self.user.to_dict(),
        }


