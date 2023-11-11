from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_post_api():
    params = {
        'title': 'test title',
        'author': 'test author',
        'description': 'test description',
        'article_image': 'test article image'
    }
    response = client.post('/api/add_post', json=params)
    assert response.status_code == 201
    assert "title" in response.json()


def test_get_books_post_method():
    response = client.post('/api/get_posts')
    assert response.status_code == 200


def test_get_posts():
    response = client.get('/api/get_posts')
    assert response.status_code == 200


def test_post_search():
    params = {
        'query_str': 'gfdgfdgfdgftdg'
    }
    response = client.get('/api/post_search', params=params)
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_post_search_success():
    params = {
        'query_str': 'test author'
    }
    response = client.get('/api/post_search', params=params)
    assert response.status_code == 200
    assert len(response.json()) > 0
