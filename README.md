# Flask-Lan

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ischaojie/flask-lan/CI?style=flat-square)
[![codecov](https://codecov.io/gh/ischaojie/flask-lan/branch/main/graph/badge.svg?token=FPBE0LGDCO)](https://codecov.io/gh/ischaojie/flask-lan)
[![PyPI](https://img.shields.io/pypi/v/flask-lan?style=flat-square)](https://pypi.org/project/Flask-Lan/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-lan?style=flat-square)
![GitHub](https://img.shields.io/github/license/ischaojie/flask-lan?style=flat-square)

Modernized Flask API builder with schema validator and OpenAPI.

### Warning

> Currently, `Flask-Lan` is still under active development(before v1.0.0).
>
> Don't use it in production.

Flask-Lan is kind of like the famous library [FastAPI](https://github.com/tiangolo/fastapi), bringing part of its brilliant features to your Flask application, you can see a lot of similarities between the two.

For example, it uses [Pydantic](https://github.com/samuelcolvin/pydantic) for request and response validation,
it will auto-generate `OpenAPI` API docs and so on.

## Feature

-   Intuitive and easy to use.
-   Request/Response validation based on type hinting(by Pydantic).
-   Auto-generated `OpenAPI` docs(both swagger and redoc).
-   Designed for API development.

## Quick start

```bash
python -m pip install Flask-Lan
```

You can view and run the code in the [example](/example/) file.
Then open [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) you will see the API docs like this:

![docs](/docs/assets/docs.png)

Read the [docs](https://flask-lan.chaojie.fun/) to get more details.

## License

This project is licensed under the terms of the MIT license.
