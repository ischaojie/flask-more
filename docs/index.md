# Overview

`flask-lan` is a schema validator and swagger generator but more modernized.

!!! Warning

    Currently, `flask-lan` is still under active development(before verion 1.0.0). Don't use it in production.

It's kind of like the famous library `FastAPI`, bringing part of brilliant features of `FastAPI` to your Flask application.
For example, it uses [Pydantic](https://github.com/samuelcolvin/pydantic) for Request/Response params validation and auto-generates `swagger` docs.

## Feature

-   Intuitive and easy to use.
-   Use type hinting to validate request/response params.
-   Auto-generate `swagger` docs.

## Install

Installation is as simple as:

```bash
pip install flask-lan
```

## Example

```python
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

```

Try this in your editor, and use view function's params for your work.

## Thanks

`flask-lan` is based on [flask](https://github.com/pallets/flask) and [pydantic](https://github.com/samuelcolvin/pydantic), thanks all of them's fantastic work.

## License

This project is licensed under the terms of the MIT license.
