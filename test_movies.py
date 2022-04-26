import pytest

import config


#instanciate app
flask_app = config.connex_app
flask_app.add_api("swagger.yml")


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c

def test_get_all_movies(client):
    response = client.get('/api/movies')
    assert response.status_code == 200