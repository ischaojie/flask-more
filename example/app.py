from flask import Flask
from flask_valid import validator

app = Flask(__name__)


@validator
@app.get("/")
def home():
    return {"msg": "Hello, World!"}


if __name__ == "__main__":
    app.run(debug=True)
