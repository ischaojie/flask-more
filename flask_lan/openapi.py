from functools import partial, wraps
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from flask import Flask, current_app, request
from pydantic import BaseModel, HttpUrl
from werkzeug.routing import Map, Rule
from flask_lan.schemas import ParameterInType

# from flask_lan.schemas import OpenAPI
from flask_lan.utils import get_f_annotations, is_f_param_required


def gen_openapi_schema(
    *,
    title: str,
    version: str,
    openapi_version: str = "3.0.2",
    desc: Optional[str] = None,
    app: Flask,
    terms: Optional[HttpUrl] = None,
    contact: Optional[Dict[str, str]] = None,
    license: Optional[Dict[str, str]] = None,
    tags: Optional[Dict[str, Any]] = None,
):
    """
    generate openapi specification
    title: openapi title
    version: current api version
    """
    map = app.url_map
    info = {
        "title": title,
        "description": desc,
        "termsOfService": terms,
        "contact": contact,
        "license": license,
        "version": version,
    }
    paths = {}
    components = {}
    schemas = {}
    view_functions = app.view_functions or {}
    docs_schema = app.extensions.get("lan", {})
    for rule in map.iter_rules():
        view_func = view_functions.get(rule.endpoint)
        params_schema = get_view_params_schema(rule, view_func, docs_schema)
        if not params_schema:
            continue
        params, schema = params_schema
        view_path = build_view_path(rule)
        paths.setdefault(view_path, {}).update(params)
        schemas.update(schema)

    components["schemas"] = schemas

    r = {
        "openapi": openapi_version,
        "info": info,
        "externalDocs": None,
        "servers": "",
        "tags": tags,
        "paths": paths,
        "components": components,
    }
    # return OpenAPI(**r).dict()


def build_view_path(rule: Rule):
    """build view router path from rule"""
    parts = []
    for is_dynamic, data in rule._trace:
        if is_dynamic:
            parts.append(f"<{data}>")
        else:
            parts.append(data)
    path = "".join(parts).lstrip("|")
    return path


def get_view_params_schema(
    rule: Rule,
    view_func: Callable,
    docs_schema: dict,
) -> Optional[tuple]:
    """
    Get path or query params and request body schema from rule.

    """
    params = {}
    schema = {}

    methods = rule.methods and rule.methods or []
    for method in methods:
        method_schema = {
            "responses": {},
        }
        method_schema.update(docs_schema.get(rule.endpoint, {}))

        # query or path params
        view_params, body_schema = _get_view_params_schema(rule, view_func)
        if view_params:
            method_schema["parameters"] = view_params
        # requestBody
        if body_schema:
            body_name, _schema = body_schema
            method_schema["requestBody"] = {
                "description": "",
                "content": {
                    "application/json": {
                        "schema": _schema,
                    },
                },
                # FIXME
                "required": True,
            }
        params[method] = method_schema
        schema[body_name] = _schema

    return params, schema


def _get_view_params_schema(rule: Rule, view_func: Callable) -> tuple:

    # path and query params
    params: list = []
    # request body schema
    body_schema: tuple = ()

    for name, _type in get_f_annotations(view_func).items():
        param: dict = {}
        # this is path params
        if name in rule.arguments:
            param["name"] = name
            param["in"] = ParameterInType.path
            param["required"] = True
            param["schema"] = {
                "type": _type.__name__,
                # TODO: schema default
            }
        # this is request body params
        elif issubclass(_type, BaseModel):
            body_schema = (name, _type.schema())
        # this all is query body
        else:
            param["name"] = name
            param["in"] = ParameterInType.query
            param["required"] = is_f_param_required
            param["schema"] = {
                "type": _type.__name__,
            }
        if param:
            params.append(param)

    return params, body_schema


def docs(
    f: Callable,
    *,
    tags: Optional[List[str]] = None,
    summary: Optional[str] = None,
    desc: Optional[str] = None,
):
    """docs decorator"""
    if f is None:
        return partial(docs, tags=tags)

    @wraps(f)
    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        config = current_app.extensions.get("lan", {})
        url_rule = request.url_rule
        if url_rule:
            doc_schema = {
                "tags": tags,
                "summary": summary,
                "description": desc,
                "operationId": url_rule.endpoint,
            }
            config.setdefault(url_rule.endpoint, {}).update(url_rule.endpoint, doc_schema)
        current_app.extensions["lan"] = config

        return r

    return wrapper
