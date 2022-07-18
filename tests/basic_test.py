import sys
sys.path.append('../flask_masque')
from app import app

def test_index_route():
    response = app.test_client().get('/')

    # print(response.data.decode('utf-8'))
    assert response.status_code == 200

test_index_route()