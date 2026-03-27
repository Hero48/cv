from flask import Blueprint, request, jsonify, session
from database import db
from models import User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
        
    user = User(email=email)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return jsonify({"message": "User created successfully", "user": {"email": email, "id": user.id}})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this email already exists"}), 400

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful", "user": {"email": email, "id": user.id}})
        
    return jsonify({"error": "Invalid email or password"}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})

@auth_bp.route('/api/me')
def me():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({"user": {"email": user.email, "id": user.id}})
    return jsonify({"user": None})
