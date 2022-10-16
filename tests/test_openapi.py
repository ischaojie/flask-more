from flask.testing import FlaskClient

from flask_lan.schemas import OpenAPI
from flask_lan.utils import get_normalize_path


def test_openapi_spec(client: FlaskClient):
    rsp = client.get("/openapi.json")
    assert rsp.status_code == 200

    openapi = OpenAPI.parse_obj(rsp.json)
    rules = [get_normalize_path(rule) for rule in client.application.url_map.iter_rules()]
    for path in openapi.paths.keys():
        assert path in rules

    echo = openapi.paths.get("/")
    assert echo.get.summary == "echo"
    assert echo.get.description == "hello echo"
    assert echo.get.tags == ["test"]


def test_swagger(client: FlaskClient):
    rsp = client.get("/docs")
    assert rsp.status_code == 200


def test_redoc(client: FlaskClient):
    rsp = client.get("/redoc")
    assert rsp.status_code == 200
