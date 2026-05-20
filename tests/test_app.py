import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = app.test_client()

def test_health():
    response = client.get('/health')
    assert response.status_code == 200

def test_metrics():
    response = client.get('/metrics')
    assert response.status_code == 200

def test_github_check():
    response = client.get('/github')
    assert response.status_code == 200