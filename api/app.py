from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy import desc
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash
import os
from config import app, db, migrate, api
from models import db, User, Shelter

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


        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        print(f"Error: {str(e)}")  # Log the error for debugging purposes
        return jsonify({'error': 'Internal server error'}), 500

        
@app.route('/login', methods=['POST'])
def login():
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

    # Update session with user_id and role
    session['user_id'] = user.id

    # Serialize user data
    user_data = user.to_dict()

    # Return serialized user data
    return jsonify({
        'message': 'Login successful',
        'user': user_data
    }), 200

   
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    # Return the user data (could be useful for testing)
    return jsonify(user.to_dict()), 200


@app.route('/shelters', methods=['GET', 'POST'])
def create_shelter():
    
    if request.method == 'GET':
        all_shelters = Shelter.query.all()
        results = []
        for shelter in all_shelters:
            results.append(shelter.to_dict())
        return results, 200
        
    # Get the user from the session
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Fetch the user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # # Check if the user is an owner
    # if user.role != 'owner':
    #     return jsonify({'error': 'User is not authorized to create a shelter'}), 403

    # If the user is an owner, proceed with shelter creation
    shelter_data = request.get_json()

    # Check for required shelter fields
    required_fields = ['shelter_name', 'shelter_email', 'shelter_phone', 'street_address', 'city', 'state', 'zipcode']
    for field in required_fields:
        if field not in shelter_data:
            return jsonify({'error': f'Missing {field} for shelter creation'}), 400

    # Create and add the shelter to the database
    new_shelter = Shelter(
        name=shelter_data['shelter_name'],
        email=shelter_data['shelter_email'],
        phone=shelter_data['shelter_phone'],
        street_address=shelter_data['street_address'],
        city=shelter_data['city'],
        state=shelter_data['state'],
        zipcode=shelter_data['zipcode'],
        about=shelter_data.get('about', ''),
        owner_id=user.id  # Link the shelter to the user (owner)
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
        
