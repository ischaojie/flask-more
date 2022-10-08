import pytest
from flask import Flask
from flask.testing import FlaskClient

from tests.app import app as _app


@pytest.fixture()
def app():
    yield _app


@pytest.fixture(autouse=True)
def client(app: Flask) -> FlaskClient:
    return app.test_client()
