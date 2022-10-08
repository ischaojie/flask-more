from flask.testing import FlaskClient


def test_gen_openapi_spec(client: FlaskClient):
    rsp = client.get("/openapi.json")
    assert rsp.status_code == 200


def test_swagger(client: FlaskClient):
    rsp = client.get("/swagger")
    assert rsp.status_code == 200


def test_redoc(client: FlaskClient):
    rsp = client.get("/redoc")
    assert rsp.status_code == 200
