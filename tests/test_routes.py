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

# Login flow
@patch('app.routes.users', {'user@site.com': 'pass'})
def test_login(client):
    response = client.post('/users/login', json={'email': 'user@site.com', 'password': 'pass'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data

# Retrieval logic
@patch('app.kb_retriever.retrieve_relevant_entries', return_value=[{'question': 'Q1', 'answer': 'A1'}])
def test_kb_retrieval(mock_retrieve):
    results = routes.retrieve_relevant_entries('dummy')
    assert results == [{'question': 'Q1', 'answer': 'A1'}]
