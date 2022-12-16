# @api

Basically, Flask-More does most of the work using the `@api` decorator, which does not disturb the existing routing view. The functionality adds validation of the request data, handles the request body data automatically, and helps you describe the api's functionality in more detail.

## Validation

```python
from flask import FLask
from flask_more import More, api
from pydantic import BaseModel
from models import User

app = Flask(__name)

More(app)


class UserSchema(BaseModel):
    name: str
    age: int


@app.post('/users')
@api
def add_user(user: UserSchema):
    new_user = user.dict()
    Users.create(**new_user)
    return new_user
```

## OpenAPI

```python
from flask import FLask
from flask_more import More, api
from pydantic import BaseModel
from models import User

app = Flask(__name)

More(app)


class UserSchema(BaseModel):
    name: str
    age: int


@app.get('/users')
@api(
    tags=["users"],
    summary="get all users",
    description="get all or query users",
)
def get_users(start: int = 0, limit: int = 10):
    pass

@app.get('/others')
@api(tags=["others"])
def others():
    pass
```
