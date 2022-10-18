from typing import Optional, cast

from flask import Flask, Response, json, jsonify, render_template_string
from werkzeug.exceptions import HTTPException

from flask_lan.openapi import gen_openapi_spec
from flask_lan.templates import redoc_template, swagger_template


class Lan:
    def __init__(
        self,
        app: Optional[Flask] = None,
        title: str = "API Docs",
        version: str = "1.0",
        docs_url: str = "/docs",
        redoc_url: str = "/redoc",
        openapi_url: str = "/openapi.json",
    ) -> None:
        self.title = title
        self.version = version
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.openapi_url = openapi_url

        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app: Flask) -> None:

        self.app.register_error_handler(HTTPException, self.handle_exception)

        if self.docs_url:
            app.add_url_rule(self.docs_url, view_func=self.docs)
        if self.redoc_url:
            app.add_url_rule(self.redoc_url, view_func=self.redoc)
        if self.openapi_url:
            app.add_url_rule(self.openapi_url, view_func=self.openapi)

    def docs(self) -> str:
        context = {"title": self.title}
        return render_template_string(swagger_template, **context)

    def redoc(self) -> str:
        context = {"title": self.title}
        return render_template_string(redoc_template, **context)

    def openapi(self) -> Response:
        self.openapi_schema = gen_openapi_spec(
            routes=self.app.url_map,
            view_functions=self.app.view_functions,
            title=self.title,
            version=self.version,
            desc="",
        )
        schema = self.openapi_schema.dict(by_alias=True, exclude_defaults=True)
        return jsonify(schema)

    def handle_exception(self, e: HTTPException) -> Response:
        rsp = cast(Response, e.get_response())
        rsp.data = json.dumps({"detail": e.description})
        rsp.content_type = "application/json"
        return rsp
