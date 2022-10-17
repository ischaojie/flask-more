from flask import Flask
from pydantic import BaseModel

from flask_lan import Lan, api

app = Flask(__name__)

Lan(app, "Book API")

books = [
    {
        "title": "The Three-Body Problem",
        "author": "liucixin",
        "price": 10.5,
    },
    {
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "price": 22,
    },
]


class BookSchema(BaseModel):
    title: str
    author: str
    price: float


@app.get("/")
@api
def home():
    return {"msg": "hello"}


@app.post("/books")
@api(tags=["books"], summary="create book")
def create_book(schema: BookSchema):
    new_book = schema.dict()
    books.append(new_book)
    return new_book


@app.get("/books")
@api(
    tags=["books"],
    summary="query book",
    description="query book by some search condition",
)
def query_book(like: str = "", start: int = 0, count: int = 10):
    r = list(filter(lambda book: like in book["title"], books))
    return {
        "start": start,
        "count": count,
        "items": r,
        "total": len(r),
    }


@app.get("/books/<title>")
@api(
    tags=["books"],
    summary="get book",
    description="get book by title",
)
def get_book(title: str):
    r = {}
    for book in books:
        if book["title"] == title:
            r = book
    return r


if __name__ == "__main__":
    app.run(debug=True)
