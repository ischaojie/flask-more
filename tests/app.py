from typing import List

from flask import Flask
from pydantic import BaseModel

from flask_lan import Lan, api

app = Flask(__name__)
app.config["TESTING"] = True

Lan(app, "Book API")


class BookSchema(BaseModel):
    title: str
    price: float


class RspSchema(BaseModel):
    start: int = 0
    count: int = 10
    items: List[BookSchema] = []


@app.get("/")
@api(tags=["test"], summary="echo", description="hello echo")
def echo():
    return {"msg": "ok"}


@app.get("/echo_status")
@api(status=400)
def echo_status():
    return {"msg": "ok"}


@app.get("/echo_path/<id>")
@api(tags=["echo_path"], description="echo_path")
def echo_path(id: int):
    return {"id": id}


@app.get("/echo_multi_path/<id>/book/<book_id>")
@api(tags=["echo_path"], description="echo_multi_path")
def echo_multi_path(id: int, book_id: int):
    return {"id": id, "book_id": book_id}


@app.get("/echo_query")
@api
def echo_query(name: str, age: int = 18):
    return {"name": name, "age": age}


@app.post("/echo_body")
@api
def echo_body(book: BookSchema):
    return dict(book)


@app.get("/echo_path_and_query/<id>")
@api
def echo_path_and_query(id: int, name: str, age: int = 18):
    return {"id": id, "name": name, "age": age}


@app.get("/echo_rsp")
@api(rsp_model=RspSchema)
def echo_rsp():
    return RspSchema(items=[BookSchema(title="test", price=1.0)])


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5001)
