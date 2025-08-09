import pytest
from flask import Flask
from app.routes import bp
import app.routes as routes
from unittest.mock import patch

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Registration flow (positive)
# Test user registration (positive)
def test_register_user(client):
    response = client.post('/users/register', json={'email': 'test@site.com', 'password': 'pass'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['message'] == 'User registered successfully.'

# Test user registration (duplicate)
def test_register_duplicate_user(client):
    client.post('/users/register', json={'email': 'dup@site.com', 'password': 'pass'})
    response = client.post('/users/register', json={'email': 'dup@site.com', 'password': 'pass'})
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data

# Test user registration (missing fields)
def test_register_missing_fields(client):
    response = client.post('/users/register', json={'email': '', 'password': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

# Login flow
def test_login(client):
    # Register user first
    client.post('/users/register', json={'email': 'user@site.com', 'password': 'pass'})
    response = client.post('/users/login', json={'email': 'user@site.com', 'password': 'pass'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data

# Test login (invalid credentials)
def test_login_invalid(client):
    client.post('/users/register', json={'email': 'bad@site.com', 'password': 'pass'})
    response = client.post('/users/login', json={'email': 'bad@site.com', 'password': 'wrong'})
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data

# Retrieval logic
@patch('app.routes.retrieve_relevant_entries', return_value=[{'question': 'Q1', 'answer': 'A1'}])
def test_kb_retrieval(mock_retrieve):
    results = routes.retrieve_relevant_entries('dummy')
    assert results == [{'question': 'Q1', 'answer': 'A1'}]

# Test /admin/users (list users)
def test_list_users(client):
    # Register two users
    client.post('/users/register', json={'email': 'a@site.com', 'password': 'pass'})
    client.post('/users/register', json={'email': 'b@site.com', 'password': 'pass'})
    # Login as admin
    login = client.post('/users/login', json={'email': 'admin@site.com', 'password': 'adminpass'})
    token = login.get_json()['token']
    response = client.get('/admin/users', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data
    assert len(data['users']) >= 3  # admin + 2 users

# Test /admin/users/<user_id> (delete user)
def test_delete_user(client):
    reg = client.post('/users/register', json={'email': 'del@site.com', 'password': 'pass'})
    user_id = reg.get_json()['id']
    # Login as admin
    login = client.post('/users/login', json={'email': 'admin@site.com', 'password': 'adminpass'})
    token = login.get_json()['token']
    response = client.delete(f'/admin/users/{user_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

# Test /admin/users/<user_id> (delete non-existent user)
def test_delete_nonexistent_user(client):
    # Login as admin
    login = client.post('/users/login', json={'email': 'admin@site.com', 'password': 'adminpass'})
    token = login.get_json()['token']
    response = client.delete('/admin/users/doesnotexist', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

# Test /test/endpoints health

# Test /chat/ (JWT required, positive)
def test_chat_with_jwt(client):
    import torch
    # Register and login to get token
    reg = client.post('/users/register', json={'email': 'chat@site.com', 'password': 'pass'})
    login = client.post('/users/login', json={'email': 'chat@site.com', 'password': 'pass'})
    token = login.get_json()['token']
    # Patch model to avoid heavy inference
    dummy_tensor = torch.tensor([[0]])
    with patch('app.routes.phi2_model.generate', return_value=dummy_tensor), \
         patch('app.routes.phi2_tokenizer.decode', return_value='Hello!'):
        response = client.post('/chat/', json={'message': 'Hi'}, headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'response' in data

# Test /chat/ (JWT required, missing)
def test_chat_missing_jwt(client):
    response = client.post('/chat/', json={'message': 'Hi'})
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
