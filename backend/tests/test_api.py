import pytest
import os
from app import create_app, db

@pytest.fixture
def app():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    """Register and login a test user, return JWT token"""
    client.post('/api/auth/register', 
        json={
            'email': 'test@example.com',
            'password': 'Test123!',
            'full_name': 'Test User'
        }
    )
    response = client.post('/api/auth/login',
        json={
            'email': 'test@example.com',
            'password': 'Test123!'
        }
    )
    return response.get_json()['access_token']


class TestAuth:
    def test_register_success(self, client):
        response = client.post('/api/auth/register',
            json={
                'email': 'newuser@example.com',
                'password': 'Password123!',
                'full_name': 'New User'
            }
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_register_duplicate_email(self, client):
        client.post('/api/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'Test123!',
                'full_name': 'Test User'
            }
        )
        response = client.post('/api/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'Test123!',
                'full_name': 'Another User'
            }
        )
        assert response.status_code == 409
    
    def test_login_success(self, client, auth_token):
        assert auth_token is not None
        assert isinstance(auth_token, str)
    
    def test_login_invalid_password(self, client):
        client.post('/api/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'Test123!',
                'full_name': 'Test User'
            }
        )
        response = client.post('/api/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'WrongPassword'
            }
        )
        assert response.status_code == 401


class TestPolicy:
    def test_create_policy(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/policies',
            json={
                'policy_type': 'Health',
                'coverage_amount': 200000,
                'monthly_premium': 50,
                'description': 'Family health coverage'
            },
            headers=headers
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['policy']['policy_type'] == 'Health'
    
    def test_get_policies(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a policy first
        client.post('/api/policies',
            json={
                'policy_type': 'Auto',
                'coverage_amount': 100000,
                'monthly_premium': 30
            },
            headers=headers
        )
        
        response = client.get('/api/policies', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['policy_type'] == 'Auto'


class TestAI:
    def test_hello_endpoint(self, client):
        response = client.get('/api/hello')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'Hello from InsureSmart AI backend' in data['message']

    def test_policy_advisor_requires_auth(self, client):
        response = client.post('/api/ai/policy-advisor', json={'user_input': 'health plan'})
        assert response.status_code == 401

    def test_policy_advisor_returns_valid_recommendation(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/ai/policy-advisor',
            json={'user_input': 'I need health insurance for my family'},
            headers=headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['provider'] in ['openai', 'fallback']
        assert 'message' in data
        assert isinstance(data['recommendations'], list)

    def test_policy_advisor_history_persists(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        advisor_response = client.post(
            '/api/ai/policy-advisor',
            json={'user_input': 'I need auto insurance for a new car'},
            headers=headers
        )
        assert advisor_response.status_code == 200

        history_response = client.get('/api/ai/history', headers=headers)
        assert history_response.status_code == 200
        history_data = history_response.get_json()
        assert len(history_data) >= 1
        assert history_data[0]['user_prompt']
