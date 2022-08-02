from flask import Flask
from pydantic import BaseModel
from flask_lan import validator

app = Flask(__name__)


class BookSchema(BaseModel):
    title: str
    author: str
    price: float
    year: int


@app.get("/books/")
@validator
def query_book(title: str, start: int = 0, limit: int = 10):
    pass


@app.get("/books/<id>/")
@validator(rsp_model=BookSchema)
def get_book(id: int):
    pass


@app.post("/books/")
@validator
def create_book(book: BookSchema):
    pass


if __name__ == "__main__":
    app.run(debug=True)
