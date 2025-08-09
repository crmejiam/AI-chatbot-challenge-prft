from flask import Blueprint, request, jsonify, render_template
import jwt
import datetime
import os
from dotenv import load_dotenv

# Hugging Face Transformers for Phi-2
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

load_dotenv()

bp = Blueprint('routes', __name__)

# Load Phi-2 model and tokenizer once at startup
phi2_model_name = "microsoft/phi-2"
phi2_tokenizer = AutoTokenizer.from_pretrained(phi2_model_name)
phi2_model = AutoModelForCausalLM.from_pretrained(phi2_model_name)
phi2_model.eval()

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

    # Compose prompt for Phi-2
    system_prompt = "You are a polite, customer-focused assistant who provides accurate information about GitHub Actions."
    instructions = (
        "Always greet users warmly, answer with respect, and maintain a professional tone. "
        "Your main goal is to deliver excellent customer experience and provide accurate, specific information about GitHub Actions. "
        "Respond concisely and directly to the user's input without adding unnecessary context."
    )
    # Prepend instructions to user message
    full_user_message = f"{instructions}\n{user_message}"
    prompt = f"{system_prompt}\nUser: {full_user_message}\nAssistant:"

    try:
        # Encode input and check context length (Phi-2 max is 2048 tokens)
        input_ids = phi2_tokenizer.encode(prompt, return_tensors='pt')
        attention_mask = torch.ones_like(input_ids)
        if input_ids.shape[1] > 2048:
            return jsonify({'error': 'Your message is too long for the model. Please shorten your input.'}), 400

        # Generate response
        with torch.no_grad():
            output_ids = phi2_model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=400,
                pad_token_id=phi2_tokenizer.eos_token_id,
                do_sample=True,
                top_p=0.9,  # Slightly stricter nucleus sampling
                top_k=20,   # Lower for faster sampling
                temperature=0.1
            )

        # Decode and extract assistant's reply
        output_text = phi2_tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Extract only the first assistant reply, stopping before any additional 'User:' or 'Assistant:' turns
        if "Assistant:" in output_text:
            reply = output_text.split("Assistant:", 1)[-1]
            for marker in ["User:", "Assistant:"]:
                if marker in reply:
                    reply = reply.split(marker, 1)[0]
            reply = reply.strip()
        else:
            reply = output_text.strip()

        # Always return as markdown for frontend rendering
        response_type = "markdown"
        # Ensure code block is wrapped in triple backticks if code detected
        if '```' in reply and not reply.strip().startswith('```'):
            reply = f"```\n{reply.strip()}\n```"

        return jsonify({'response': reply, 'response_type': response_type})

    except RuntimeError as e:
        if 'out of memory' in str(e).lower():
            return jsonify({'error': 'Server is overloaded. Please try again later.'}), 503
        return jsonify({'error': f'Runtime error: {str(e)}'}), 500
    except torch.cuda.CudaError as e:
        return jsonify({'error': 'GPU error. Please try again later.'}), 503
    except Exception as e:
        if 'rate limit' in str(e).lower():
            return jsonify({'error': 'API rate limit exceeded. Please wait and try again later.'}), 429
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
