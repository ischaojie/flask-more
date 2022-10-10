# Flask-Lan

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ischaojie/flask-lan/CI?style=flat-square)
![Codecov](https://img.shields.io/codecov/c/github/ischaojie/flask-lan?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/flask-lan?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-lan?style=flat-square)
![GitHub](https://img.shields.io/github/license/ischaojie/flask-lan?style=flat-square)

Modernized Flask API builder with schema validator and OpenAPI.

### Warning
> 
> Currently, `Flask-Lan` is still under active development(before v1.0.0). Don't use it in production.

It's kind of like the famous library [FastAPI](https://github.com/tiangolo/fastapi), bringing part of brilliant features of `FastAPI` to your Flask application.
For example, it uses [Pydantic](https://github.com/samuelcolvin/pydantic) for Request/Response params validation 
and auto-generates `OpenAPI` api docs.

## Feature

-   Intuitive and easy to use.
-   Request/Response validation base on type hinting(by Pydantic).
-   Auto-generate `OpenAPI` docs(both swagger and redoc).

## Quick start

```bash
pip install Flask-Lan
```

A simple example:

```python
from flask import Flask
from pydantic import BaseModel

from flask_lan import Lan, validator

app = Flask(__name__)

Lan(app, "Book API")


class BookSchema(BaseModel):
    title: str
    price: float

@app.get("/books/<id>")
@validator
def example(id: int, hi: str, book: BookSchema):
    return book.dict()

if __name__ == "__main__":
    app.run(debug=True)


```
Then open `http://127.0.0.1:5000/swagger` you will seen the api docs.

## License

This project is licensed under the terms of the MIT license.
