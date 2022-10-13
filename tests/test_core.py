from flask.testing import FlaskClient


def test_json_rsp(client: FlaskClient):
    rsp = client.get("/invalid")
    assert rsp.status_code == 404
    assert rsp.content_type == "application/json"
    data = rsp.get_json() or {}
    assert "detail" in data
