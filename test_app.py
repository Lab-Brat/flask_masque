import pytest
import json
from app import create_app

app = create_app()
print(type(app))

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    print(response.data.decode('utf-8'))

test_index_route()