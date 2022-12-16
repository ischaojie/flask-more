# Flask-More

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ischaojie/flask-more/ci.yml?branch=main&style=flat-square)
[![codecov](https://codecov.io/gh/ischaojie/flask-more/branch/main/graph/badge.svg?token=FPBE0LGDCO)](https://codecov.io/gh/ischaojie/flask-more)
[![PyPI](https://img.shields.io/pypi/v/flask-more?style=flat-square)](https://pypi.org/project/Flask-More/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-more?style=flat-square)
![GitHub](https://img.shields.io/github/license/ischaojie/flask-more?style=flat-square)

Modernized Flask API builder with schema validator and OpenAPI.


> **Warning**
>
> Currently, `Flask-More` is still under active development(before v1.0.0).
>
> Don't use it in production.

Flask-More is kind of like the famous library [FastAPI](https://github.com/tiangolo/fastapi), bringing part of its brilliant features to your Flask application, you can see a lot of similarities between the two.

For example, it uses [Pydantic](https://github.com/samuelcolvin/pydantic) for request and response validation,
it will auto-generate `OpenAPI` API docs and so on.

## Feature

-   Intuitive and easy to use.
-   Request/Response validation based on type hinting(by Pydantic).
-   Auto-generated `OpenAPI` docs(both swagger and redoc).
-   Designed for API development.

## Quick start

```bash
python -m pip install Flask-More
```

You can view and run the code in the [example](/example/) file.
Then open [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) you will see the API docs like this:

![docs](https://img.chaojie.fun/flask-more-docs.png)

Read the [docs](https://flask-more.chaojie.fun/) to get more details.

## License

This project is licensed under the terms of the MIT license.
