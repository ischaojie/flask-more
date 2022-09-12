def test_validator(client):
    rsp = client.get("/")
    assert rsp.status_code == 200
    assert rsp.json["msg"] == "ok"


def test_validate_path(client):
    rsp = client.get("/echo_path/1")
    assert rsp.status_code == 200
    assert rsp.json["id"] == 1


def test_validate_multi_path(client):
    rsp = client.get("/echo_multi_path/1/book/2")
    assert rsp.status_code == 200
    assert rsp.json["id"] == 1
    assert rsp.json["book_id"] == 2


def test_invalidate_path(client):
    rsp = client.get("/echo_path/a")
    assert rsp.status_code == 400


def test_validate_query(client):
    rsp = client.get("/echo_query?name=test&age=1")
    assert rsp.status_code == 200
    assert rsp.json["name"] == "test"
    assert rsp.json["age"] == 1


def test_validate_query_default(client):
    rsp = client.get("/echo_query")
    assert rsp.status_code == 200
    assert rsp.json["name"] == "chaojie"
    assert rsp.json["age"] == 18


def test_invalidate_query(client):
    rsp = client.get("/echo_query?name=test&age=a")
    assert rsp.status_code == 400


def test_validate_body(client):
    rsp = client.post("/echo_body", json={"title": "test", "price": 1.0})
    assert rsp.status_code == 200
    assert rsp.json["title"] == "test"
    assert rsp.json["price"] == 1.0


def test_validate_body_empty(client):
    rsp = client.post("/echo_body")
    assert rsp.status_code == 400


def test_invalid_body(client):
    rsp = client.post("/echo_body", json={"title": "test", "price": "invalid"})
    assert rsp.status_code == 400
    assert "price" in rsp.json["details"][0]["loc"]


def test_validate_path_and_query(client):
    rsp = client.get("/echo_path_and_query/1?name=test&age=1")
    assert rsp.status_code == 200
    assert rsp.json["id"] == 1
    assert rsp.json["name"] == "test"
    assert rsp.json["age"] == 1


def test_validate_status(client):
    rsp = client.get("/echo_status")
    assert rsp.status_code == 400
