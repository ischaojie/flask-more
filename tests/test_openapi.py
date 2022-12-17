from flask import Flask
from flask.testing import FlaskClient
from openapi_spec_validator import validate_spec

from flask_more.openapi import make_schemas
from flask_more.schemas import OpenAPI
from flask_more.utils import get_normalize_path


def test_docs(client: FlaskClient) -> None:
    rsp = client.get("/docs")
    assert rsp.status_code == 200


def test_redoc(client: FlaskClient) -> None:
    rsp = client.get("/redoc")
    assert rsp.status_code == 200


def validate_openapi_schema(client: FlaskClient) -> None:
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert validate_spec(resp.json) is None


def test_openapi_spec(client: FlaskClient) -> None:
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


def test_openapi_nested_schemas(client: FlaskClient) -> None:
    rsp = client.get("/openapi.json")
    openapi = OpenAPI.parse_obj(rsp.json)

    all_schemas = ["Author", "BookSchema", "MovieSchema"]
    for schema in openapi.components.schemas.keys():
        assert schema in all_schemas


def test_make_schemas(app: Flask) -> None:
    should_maked_schemas = ("Author", "BookSchema", "MovieSchema")
    schemas = make_schemas(app.url_map.iter_rules(), app.view_functions)
    for schema in schemas:
        assert schema in should_maked_schemas
