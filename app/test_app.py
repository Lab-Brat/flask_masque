# Unit test for flask application
from app import create_app

app = create_app()
print(type(app))


def test_index_route():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_form_route():
    response = app.test_client().get("/form")
    assert response.status_code == 200


def test_unit_route():
    response = app.test_client().get("/unit")
    assert response.status_code == 200
