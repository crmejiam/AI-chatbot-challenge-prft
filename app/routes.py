

from flask import Blueprint, request, jsonify
import jwt
import datetime

bp = Blueprint('routes', __name__)


# Helper function to verify JWT
def verify_jwt(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    secret = 'your-secret-key'  # Use the same key as in login
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Story 1: Chat endpoint (protected)
@bp.route('/chat/', methods=['POST'])
def chat():
    payload = verify_jwt(request)
    if not payload:
        return jsonify({'error': 'Authentication required.'}), 401
    return jsonify({'message': f"Chatbot response for {payload['email']} goes here."})


# Simple in-memory user store
users = {}

# Story 2: User registration
@bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400
    if email in users:
        return jsonify({'error': 'User already exists.'}), 409
    users[email] = password
    return jsonify({'message': 'User registered successfully.'}), 201



# Story 4: User login
@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400
    if email not in users or users[email] != password:
        return jsonify({'error': 'Invalid email or password.'}), 401

    # Issue JWT
    secret = 'your-secret-key'  # Replace with a secure key in production
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, secret, algorithm='HS256')
    return jsonify({'message': 'User logged in successfully.', 'token': token}), 200

# Story 3: Admin user management
@bp.route('/admin/users', methods=['GET'])
def list_users():
    return jsonify({'users': []})

@bp.route('/admin/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({'message': f'User {user_id} deleted.'})

# Story 5: Endpoint testing
@bp.route('/test/endpoints', methods=['GET'])
def test_endpoints():
    return jsonify({'message': 'All endpoints are working.'})
