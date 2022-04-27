import sys
import os
import pytest

current = os.path.dirname(os.path.realpath(__file__))
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

#directors
def test_get_all_directors(client):
    response = client.get('/api/directors')
    assert response.status_code == 200

def test_case_get_all_directors_with_limit_offset(client):
    response = client.get('/api/directors?limit=2&offset=2')
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["data"] is not None

#movies
def test_get_all_movies(client):
    response = client.get('/api/movies')    
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["data"] is not None

def test_case_get_all_movies_with_limit_offset(client):
    response = client.get('/api/movies?limit=2&offset=2')
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["data"] is not None

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
            "uid": 9167238,
            "vote_average": 0,
            "vote_count": 0
    })
    assert response.status_code == 201
