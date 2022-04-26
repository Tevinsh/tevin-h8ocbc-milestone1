import sys
import os
import pytest

current = os.getcwd()
parent = os.path.dirname(current)
sys.path.append(parent)

import config


#instanciate app
flask_app = config.connex_app
flask_app.add_api("swagger.yml")


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c

def test_get_all_directors(client):
    response = client.get('/api/directors')
    assert response.status_code == 200

def test_get_all_movies(client):
    response = client.get('/api/movies')
    assert response.status_code == 200

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_post_movies(client):
    response = client.post('/api/movies/5974', json={
            "budget": 0,
            "original_title": "string",
            "overview": "string",
            "popularity": 0,
            "release_date": "string",
            "revenue": 0,
            "tagline": "string",
            "title": "string",
            "uid": 19823,
            "vote_average": 0,
            "vote_count": 0
    })
    assert response.status_code == 201
