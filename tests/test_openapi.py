from flask_lan.openapi import _get_view_params_schema
from flask_lan.schemas import Parameter, Schema
from flask_lan.utils import get_f_defaults
from flask import Flask
import pytest
from pydantic import ValidationError
from tests.app import BookSchema


@pytest.mark.parametrize(
    "endpoint,params,body_schema",
    [
        (
            "echo_path_and_query",
            [
                {"name": "id", "in": "path", "required": True, "schema": {"type": "int"}},
                {"name": "name", "in": "query", "required": True, "schema": {"type": "str"}},
                {"name": "age", "in": "query", "required": False, "schema": {"type": "int"}},
            ],
            (),
        ),
        ("echo_body", [], ("book", BookSchema.schema())),
    ],
)
def test_get_view_params_schema(app: Flask, endpoint, params, body_schema):
    with app.app_context():
        view_func = app.view_functions.get(endpoint)
        rule = list(app.url_map.iter_rules(endpoint=endpoint))[0]
        _params, _body_schema = _get_view_params_schema(rule, view_func)
        assert _params == params
        assert _body_schema == body_schema
