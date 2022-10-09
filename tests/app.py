from typing import List

from flask import Flask
from pydantic import BaseModel

from flask_lan import Lan, validator

app = Flask(__name__)
app.config["TESTING"] = True

api = Lan(app, "Book API")


class BookSchema(BaseModel):
    title: str
    price: float


class RspSchema(BaseModel):
    start: int = 0
    count: int = 10
    items: List[BookSchema] = []


@app.get("/")
@validator
def echo():
    return {"msg": "ok"}


@app.get("/echo_status")
@validator(status=400)
def echo_status():
    return {"msg": "ok"}


@app.get("/echo_path/<id>")
@validator()
def echo_path(id: int):
    return {"id": id}


@app.get("/echo_multi_path/<id>/book/<book_id>")
@validator()
def echo_multi_path(id: int, book_id: int):
    return {"id": id, "book_id": book_id}


@app.get("/echo_query")
@validator()
def echo_query(name: str = "chaojie", age: int = 18):
    return {"name": name, "age": age}


@app.post("/echo_body")
@validator()
def echo_body(book: BookSchema):
    return dict(book)


@app.get("/echo_path_and_query/<id>")
@validator()
def echo_path_and_query(id: int, name: str, age: int = 18):
    return {"id": id, "name": name, "age": age}


@app.get("/echo_rsp")
@validator(rsp_model=RspSchema)
def echo_rsp():
    return RspSchema(items=[BookSchema(title="test", price=1.0)])
