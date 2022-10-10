from typing import Optional

from flask import Flask, jsonify, render_template_string

from flask_lan.openapi import gen_openapi_spec
from flask_lan.templates import redoc_template, swagger_template


class Lan:
    def __init__(
        self,
        app: Optional[Flask] = None,
        title: str = "API Docs",
        version: str = "1.0",
        docs_url: str = "/swagger",
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

    def init_app(self, app: Flask):
        # register docs router
        if self.docs_url:
            app.add_url_rule(self.docs_url, view_func=self.swagger)
        if self.redoc_url:
            app.add_url_rule(self.redoc_url, view_func=self.redoc)
        # register openapi router
        if self.openapi_url:
            app.add_url_rule(self.openapi_url, view_func=self.openapi)

    def init_template_engine(self):
        pass

    def swagger(self):
        context = {"title": self.title}
        return render_template_string(swagger_template, **context)

    def redoc(self):
        context = {"title": self.title}
        return render_template_string(redoc_template, **context)

    def openapi(self):
        self.openapi_schema = gen_openapi_spec(
            routes=self.app.url_map,
            view_functions=self.app.view_functions,
            title=self.title,
            version=self.version,
            desc="",
        )
        schema = self.openapi_schema.dict(by_alias=True, exclude_defaults=True)
        return jsonify(schema)
