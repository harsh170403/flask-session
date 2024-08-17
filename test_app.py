import pytest
from flask import session
from app import app  # Assuming your Flask app is in a file named app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_get(client):
    """Test the index page GET request."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Invalid password' not in response.data

def test_index_post_valid_password(client):
    """Test POST request to index with the correct password."""
    response = client.post('/', data={'username': 'test_user', 'password': 'password'})
    assert response.status_code == 302  # Redirect to /protected
    assert session['user'] == 'test_user'

def test_index_post_invalid_password(client):
    """Test POST request to index with an invalid password."""
    response = client.post('/', data={'username': 'test_user', 'password': 'wrong_password'})
    assert response.status_code == 200  # Stay on the same page
    assert b'Invalid password' in response.data

def test_protected_logged_in(client):
    """Test accessing the protected route when logged in."""
    with client.session_transaction() as sess:
        sess['user'] = 'test_user'
    response = client.get('/protected')
    assert response.status_code == 200
    assert b'test_user' in response.data

def test_protected_not_logged_in(client):
    """Test accessing the protected route when not logged in."""
    response = client.get('/protected')
    assert response.status_code == 302  # Redirect to /

def test_dropsession(client):
    """Test the dropsession route."""
    with client.session_transaction() as sess:
        sess['user'] = 'test_user'
    response = client.get('/dropsession')
    assert response.status_code == 302  # Redirect to /
    assert 'user' not in session
