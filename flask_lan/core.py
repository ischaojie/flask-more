from flask import Flask, render_template, jsonify
from typing import Optional
from flask_lan.openapi import gen_openapi_schema


class Lan:
    def __init__(
        self,
        app: Optional[Flask] = None,
        title: str = "Flask-Lan",
        version: str = "1.0",
        docs_url: str = "/docs",
        openapi_url: str = "/openapi.json",
    ) -> None:
        self.title = title
        self.version = version
        self.docs_url = docs_url
        self.openapi_url = openapi_url

        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app: Flask):
        # register docs router
        if self.docs_url:
            app.add_url_rule(self.docs_url, view_func=self.docs)
        # register openapi router
        if self.openapi_url:
            app.add_url_rule(self.openapi_url, view_func=self.openapi)

    def docs(self):
        context = {}
        return render_template("docs.html", context=context)

    def openapi(self):
        self.openapi_schema = gen_openapi_schema(
            title=self.title,
            version=self.version,
            desc="",
            app=self.app,
            contact={},
            license={},
        )
        return jsonify(self.openapi_schema)
