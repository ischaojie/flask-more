from flask import Flask
from pydantic import BaseModel

from flask_lan import Lan, api

app = Flask(__name__)

Lan(app, "Book API")


class BookSchema(BaseModel):
    title: str
    price: float

@app.get("/books/<id>")
@api(tags=["book"], summary="book example")
def example(id: int, hi: str, book: BookSchema):
    return {"id": id, "hi": hi, "book": book.dict()}

if __name__ == "__main__":
    app.run(debug=True)
