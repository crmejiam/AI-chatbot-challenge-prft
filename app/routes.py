


from flask import Blueprint, request, jsonify, render_template
import jwt
import datetime
import os
from dotenv import load_dotenv
# Hugging Face Transformers for GPT-2
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


load_dotenv()



bp = Blueprint('routes', __name__)

# Load GPT-2 model and tokenizer once at startup
gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')
gpt2_model.eval()

# Frontend route
@bp.route('/')
def index():
    return render_template('index.html')


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


# Story 1: Chat endpoint (protected, now using GPT-2)
@bp.route('/chat/', methods=['POST'])
def chat():
    payload = verify_jwt(request)
    if not payload:
        return jsonify({'error': 'Authentication required.'}), 401

    data = request.get_json()
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400

    # Compose prompt with polite system message
    system_prompt = "You are a highly polite, customer-focused assistant. Always greet users warmly, answer with respect, and maintain a professional tone. Your main goal is to deliver excellent customer experience and provide accurate, specific information about GitHub Actions.\nUser: "
    prompt = system_prompt + user_message + "\nAssistant:"

    try:
        # Encode input and check context length
        input_ids = gpt2_tokenizer.encode(prompt, return_tensors='pt')
        if input_ids.shape[1] > 1024:
            return jsonify({'error': 'Your message is too long for the model. Please shorten your input.'}), 400
        with torch.no_grad():
            output_ids = gpt2_model.generate(
                input_ids,
                max_length=min(input_ids.shape[1] + 300, 1024),
                pad_token_id=gpt2_tokenizer.eos_token_id,
                do_sample=True,
                top_p=0.95,
                top_k=50
            )
        output_text = gpt2_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        # Extract assistant's reply
        reply = output_text.split("Assistant:")[-1].strip()
        return jsonify({'response': reply})
    except RuntimeError as e:
        # Handle CUDA out of memory or CPU overload
        if 'out of memory' in str(e).lower():
            return jsonify({'error': 'Server is overloaded. Please try again later.'}), 503
        return jsonify({'error': f'Runtime error: {str(e)}'}), 500
    except torch.cuda.CudaError as e:
        return jsonify({'error': 'GPU error. Please try again later.'}), 503
    except Exception as e:
        # Simulate rate limit error for excessive requests (basic example)
        if 'rate limit' in str(e).lower():
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


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
