# =============================================================================
# Part 6: Authentication Helpers (with @token_required decorator)
# =============================================================================

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = "your-secret-key-change-in-production"
TOKEN_EXPIRATION_HOURS = 24


# =============================================================================
# PASSWORD FUNCTIONS
# =============================================================================

def hash_password(password):
    return generate_password_hash(password)


def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)


# =============================================================================
# JWT TOKEN FUNCTIONS
# =============================================================================

def create_token(user_id, is_admin=False):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None


# =============================================================================
# @token_required DECORATOR
# =============================================================================
# This is the key addition in Part 6!
# A decorator is a function that wraps another function.
#
# Usage:
#   @app.route('/api/todos')
#   @token_required
#   def get_todos(current_user):
#       # current_user is automatically passed by the decorator
#       return todos for current_user

def token_required(f):
    """
    Decorator to protect routes.

    How it works:
    1. Checks for Authorization header
    2. Extracts and validates the JWT token
    3. Fetches user from database
    4. Passes user as first argument to the route function

    If token is missing/invalid, returns 401 error.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if Authorization header exists
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token is missing'}), 401

        # Extract token from "Bearer <token>"
        try:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'error': 'Invalid token format'}), 401

        # Decode and validate token
        data = decode_token(token)
        if not data:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        # Get user from database
        from models import User
        current_user = User.query.get(data['user_id'])
        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        # Call the original function with current_user
        return f(current_user, *args, **kwargs)

    return decorated
