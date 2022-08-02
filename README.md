# Flask-Lan

`Flask-Lan` is a schema validator and swagger generator but more modernized.

!!! Warning

    Currently, `flask-lan` is still under active development(before verion 1.0.0). Don't use it in production.

It's kind of like the famous library `FastAPI`, bringing part of brilliant features of `FastAPI` to your Flask application.
For example, it uses [Pydantic](https://github.com/samuelcolvin/pydantic) for Request/Response params validation and auto-generates `swagger` docs.

## Feature

-   Intuitive and easy to use.
-   Use type hinting to validate request/response params.
-   Auto-generate `swagger` docs.

## Quick start

```bash
pip install flask-lan
```

A simple example:

```python
from flask import Flask
from pydantic import BaseModel
from flask_lan import validator, docs

app = Flask(__name__)


@docs(tag="books", desc="Get books")
@app.get("/books/<id>/")
@validator
def home(id:int, q: str, star: float=10):
    return {"id":id, "q": q, "star": star}

if __name__ == "__main__":
    app.run(debug=True)

```

## License

This project is licensed under the terms of the MIT license.
