import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirect to /add or /view
