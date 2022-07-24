import pytest

from tests.app import app as _app


@pytest.fixture()
def app():
    yield _app


@pytest.fixture(autouse=True)
def client(app):
    return app.test_client()
