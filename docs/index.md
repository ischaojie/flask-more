# Overview

!!! Warning

    Currently, `flask-valid` is still under active development(before verion 1.0.0). Don't use it in production.

`flask-valid` is a Flask request and response validator use pydantic.

Basically, you just need add `validator` decorator to your view function,
`flask-valid` will auto validate params data and rsponse data for you.

It's kind of like famous library `FastAPI`, bring part of brilliant features of `FastAPI` to your Flask application.

## Feature

-   Intuitive and easy to use.
-   Use type hinting to validate path + query + body params.

## Install

Installation is as simple as:

```bash
pip install flask-valid
```

## Example

```python
from flask import Flask
from pydantic import BaseModel
from flask_valid import validator

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

```

Try this in your editor, and use view function's params for your work.

## Thanks

`flask-valid` is based on [flask](https://github.com/pallets/flask) and [pydantic](https://github.com/samuelcolvin/pydantic), thanks all of them's fantastic work.

## License

This project is licensed under the terms of the MIT license.
