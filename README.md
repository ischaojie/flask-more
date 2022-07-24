# flask-valid

Flask request and response validator use pydantic.

## Quick start

```bash
pip install flask-valid
```

After that, you can import `validator` from `flask_valid`, and use it in your `views`.

A simple example:

```python
from flask import Flask
from pydantic import BaseModel
from flask_valid import validator

app = Flask(__name__)

class BookSchema(BaseModel):
    title: str
    star: float
    author: str


@app.get("/books")
@validator
def get_books(q: str, star: float=10):
    return {"q": q, "star": star}

@app.get("/books/<id>")
@validator(rsp_model=BookSchema)
def get_book(id: int):
    return {
        "title": "The Great Gatsby",
        "star": "10",
        "author": "F. Scott Fitzgerald",
    }

if __name__ == "__main__":
    app.run(debug=True)

```
