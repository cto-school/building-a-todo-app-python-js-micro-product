import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify

SECRET_KEY = 'your-secret-key-change-in-production'

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token is missing'}), 401

        auth_header = request.headers['Authorization']

        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid token format'}), 401

        token = auth_header.split(' ')[1]
        user_id = decode_token(token)

        if not user_id:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        from models import User
        current_user = User.query.get(user_id)

        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
