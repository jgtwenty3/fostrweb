from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy import desc
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash
import os
from config import app, db, migrate, api
from models import db, User, Shelter, Animal, MedicalRecord
from datetime import datetime


def home():
    return ''

@app.route('/sign-up', methods=['POST'])
def signup():
    data = request.get_json()

    # Check for user email
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': "Email already exists"}), 400

    # Check for required fields
    required_fields = ['first_name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400

    try:
        # Create new user
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            role=data.get('role', 'user')
        )

        # Set the user's password hash
        new_user.set_password(data['password'])

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        # Store user ID in session
        session['user_id'] = new_user.id


        return jsonify({'message': 'User created successfully','user_id': session.get('user_id')}), 201

    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        print(f"Error: {str(e)}")  # Log the error for debugging purposes
        return jsonify({'error': 'Internal server error'}), 500

        
@app.route('/login', methods=['POST'])
def login():
    # Print session ID before login
    print(f"Session ID before login: {session}")

    data = request.get_json()

    # Validate required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Authenticate user
    if not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Print session contents before setting
    print(f"Session before setting: {session}")

    # Update session with user_id and role
    session['user_id'] = user.id
    session['user_role'] = user.role.value 

    # Print session contents after setting
    print(f"Session after setting: {session}")

    # Serialize user data
    user_data = user.to_dict()

    # Return serialized user data
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role.value
        }
    }), 200


   
@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        # User is logged in, return user data or status
        return jsonify({
            'message': 'Session active',
            'user_id': session['user_id'],
            'user_role': session['user_role']
        })
    else:
        # No session, return unauthorized
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/logout', methods = ['DELETE'])
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)

    return {}, 204

@app.route('/shelters', methods=['GET', 'POST'])
def all_shelters():
    
    if request.method == 'GET':
        all_shelters = Shelter.query.all()
        results = []
        for shelter in all_shelters:
            results.append(shelter.to_dict())
        return results, 200
        
    # Get the user from the session
    if request.method == "POST":
        user_id = session.get('user_id')
        user_role = session.get('user.role')
        print("Session user_id:", user_id)  # Log user_id
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        # Fetch the user from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        shelter_data = request.get_json()
        

        # Check for required shelter fields
        required_fields = ['name', 'email', 'phone', 'street_address', 'city', 'state', 'zipcode']
        for field in required_fields:
            if field not in shelter_data:
                return jsonify({'error': f'Missing {field} for shelter creation'}), 400

        # Create and add the shelter to the database
        new_shelter = Shelter(
            name=shelter_data['name'],
            email=shelter_data['email'],
            phone=shelter_data['phone'],
            street_address=shelter_data['street_address'],
            city=shelter_data['city'],
            state=shelter_data['state'],
            zipcode=shelter_data['zipcode'],
            about=shelter_data.get('about', ''),
            workers = [user]
        )
        db.session.add(new_shelter)
        db.session.commit()

        return jsonify({'message': 'Shelter created successfully'}), 201

@app.route('/shelters/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def shelter_by_id(id):
    
    shelter = Shelter.query.filter(Shelter.id == id).first()
    
    if shelter is None:
        return {'error': "Shelter not found"}, 404
    
    if request.method == 'GET':
        return shelter.to_dict(),200
    
    elif request.method == 'DELETE':
        db.session.delete(shelter)
        db.session.commit()
        return {}, 204
    
    elif request.method == "PATCH":
        data = request.get_json()
        
        for field in data: 
            setattr(shelter, field, data[field])
        
        db.session.add(shelter)
        db.session.commit()
    
    return shelter.to_dict(), 200
        
from datetime import datetime

@app.route('/animals', methods = ['GET', 'POST'])
def all_animals():
    
    if request.method == 'GET':
        all_animals = Animal.query.all()
        results = [animal.to_dict() for animal in all_animals]
        return jsonify(results), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Convert rescue_date string to a datetime object if provided
        rescue_date_str = data.get('rescue_date')
        if rescue_date_str:
            rescue_date = datetime.strptime(rescue_date_str, '%Y-%m-%dT%H:%M:%SZ')
        else:
            rescue_date = datetime.utcnow()  # Default to current time if no rescue_date is provided
        
        # Create a new Animal instance from the request data
        new_animal = Animal(
            name=data.get('name'),
            rescue_date=rescue_date,
            rescue_info=data.get('rescue_info'),
            species=data.get('species'),
            breed=data.get('breed'),
            age=data.get('age'),
            sex=data.get('sex'),
            weight=data.get('weight'),
            description=data.get('description'),
            special_needs=data.get('special_needs'),
            status=data.get('status'),
            shelter_id=data.get('shelter_id'),
        )
        
        db.session.add(new_animal)
        db.session.commit()
        
        return jsonify(new_animal.to_dict()), 201


@app.route('/animals/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    if animal is None: 
        return {'error': "Animal not found"}, 404
    
    if request.method == 'GET':
        return animal.to_dict(), 200
    
    elif request.method == "DELETE": 
        db.session.delete(animal)
        db.session.commit()
        return (), 204
    
    elif request.method == "PATCH": 
        data = request.get_json()
        
        # Handle rescue_date field conversion if it's provided
        if 'rescue_date' in data:
            rescue_date_str = data.get('rescue_date')
            if rescue_date_str:
                try:
                    # Convert the string to a datetime object
                    rescue_date = datetime.strptime(rescue_date_str, '%Y-%m-%dT%H:%M:%SZ')
                    animal.rescue_date = rescue_date
                except ValueError:
                    return {'error': 'Invalid date format for rescue_date. Use ISO 8601 format.'}, 400
        
        # Update other fields
        for field in data:
            if field != 'rescue_date':  # Don't overwrite rescue_date here since we handled it separately
                setattr(animal, field, data[field])
        
        db.session.add(animal)
        db.session.commit()
    
    return animal.to_dict(), 200

@app.route('/animals/<int:animal_id>/medical_records', methods=['GET', 'POST'])
def manage_medical_records(animal_id):
    # Retrieve the animal
    animal = Animal.query.get(animal_id)
    if not animal:
        return {'error': "Animal not found"}, 404
    
    if request.method == "GET":
        # Fetch medical records for the specific animal
        medical_records = MedicalRecord.query.filter_by(animal_id=animal_id).all()
        return jsonify([record.to_dict() for record in medical_records]), 200
    
    if request.method == "POST":
        # Get data from the request
        data = request.get_json()

        # Check for required fields
        required_fields = ["diagnosis", "treatment", "date_of_record"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 400

        # Function to safely parse dates
        def parse_date(date_str, field_name):
            if date_str:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    return {'error': f'Invalid date format for {field_name}. Use ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS)'}, 400
            return None

        # Parse the dates
        date_of_record = parse_date(data.get('date_of_record'), 'date_of_record')
        rabies_date = parse_date(data.get('rabies_date'), 'rabies_date')
        snap_date = parse_date(data.get('snap_date'), 'snap_date')
        dhpp_date = parse_date(data.get('dhpp_date'), 'dhpp_date')

        # Check if any date parsing returned an error
        for date_field in [date_of_record, rabies_date, snap_date, dhpp_date]:
            if isinstance(date_field, tuple):  # Means an error occurred
                return date_field

        # Create new medical record
        new_record = MedicalRecord(
            animal_id=animal.id,
            diagnosis=data['diagnosis'],
            treatment=data['treatment'],
            allergies=data.get('allergies'),
            existing_conditions=data.get('existing_conditions'),
            rabies_shot=data.get('rabies_shot'),
            rabies_date=rabies_date,
            snap_shot=data.get('snap_shot'),
            snap_date=snap_date,
            dhpp_shot=data.get('dhpp_shot'),
            dhpp_date=dhpp_date,
            date_of_record=date_of_record
        )

        db.session.add(new_record)
        db.session.commit()
        return jsonify(new_record.to_dict()), 201


@app.route('/animals/<int:animal_id>/medical_records/<int:medical_record_id>', methods=['GET', 'PATCH', 'DELETE'])
def edit_medical_records(animal_id, medical_record_id):
    # Fetch the animal
    animal = Animal.query.get(animal_id)
    if not animal:
        return {'error': 'Animal not found'}, 404

    # Fetch the medical record for the specific animal
    medical_record = MedicalRecord.query.filter_by(id=medical_record_id, animal_id=animal_id).first()
    if not medical_record:
        return {'error': 'Medical record not found'}, 404
    
    # GET method to retrieve the medical record
    if request.method == 'GET':
        return jsonify(medical_record.to_dict()), 200

    # PATCH method to update the medical record
    if request.method == 'PATCH':
        data = request.get_json()

        # Function to safely parse dates
        def parse_date(date_str):
            if date_str:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    return None
            return None

        # Convert date fields to datetime objects if they exist
        if 'rabies_date' in data:
            data['rabies_date'] = parse_date(data['rabies_date'])
        if 'snap_date' in data:
            data['snap_date'] = parse_date(data['snap_date'])
        if 'dhpp_date' in data:
            data['dhpp_date'] = parse_date(data['dhpp_date'])
        if 'date_of_record' in data:
            data['date_of_record'] = parse_date(data['date_of_record'])

        # Optionally, update fields of the medical record
        for key, value in data.items():
            if hasattr(medical_record, key):
                setattr(medical_record, key, value)

        # Manually update the "updated_at" field
        medical_record.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify(medical_record.to_dict()), 200

    # DELETE method to remove the medical record
    if request.method == 'DELETE':
        db.session.delete(medical_record)
        db.session.commit()
        return jsonify({'message': 'Medical record deleted successfully'}), 200

