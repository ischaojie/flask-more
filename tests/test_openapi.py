from flask.testing import FlaskClient


def test_gen_openapi_spec(client: FlaskClient):
    rsp = client.get("/openapi.json")
    assert rsp.status_code == 200
