from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_post_api():
    params = {
        'title': 'test title',
        'author': 'test author',
        'description': 'test description'
    }
    response = client.post('/api/add_post', json=params)
    assert response.status_code == 201
    assert "title" in response.json()


def test_get_posts():
    response = client.get('/api/get_posts')
    assert response.status_code == 200


def test_record_search():
    params = {
        'query_str': 'test'
    }
    response = client.get('/api/record_search', params=params)
    assert response.status_code == 200
