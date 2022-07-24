import inspect
import sys
from functools import partial, wraps
from inspect import signature
from typing import Callable

from flask import jsonify, request
from pydantic import BaseModel, ValidationError, parse_obj_as

if sys.version_info >= (3, 10):
    from inspect import get_annotations


def get_f_annotations(f):
    try:
        return get_annotations(f)
    except NameError:
        return f.__annotations__


def get_f_defaults(f: Callable):
    """get func default params"""
    sig = signature(f)
    for k, v in sig.parameters.items():
        if v.default is not inspect.Parameter.empty:
            yield k, v.default


def validator(
    f: Callable = None,
    *,
    rsp_model=None,
    status: int = 200,
):
    if f is None:
        return partial(validator, rsp_model=rsp_model, status=status)

    @wraps(f)
    def wrapper(*args, **kwargs):

        errors = {"details": []}

        # all validated func params
        validated = {}

        # func default params
        f_defaults = dict(get_f_defaults(f))

        # current view func's url rule args
        current_f_path_params = request.url_rule.arguments

        for name, type_ in get_f_annotations(f).items():
            # validate path params
            if name in current_f_path_params:
                try:
                    value = parse_obj_as(type_, kwargs.get(name))
                    validated[name] = value
                except ValidationError as e:
                    for err in e.errors():
                        err["loc"] = ("path", name)
                        errors["details"].append(err)
            elif issubclass(type_, BaseModel):
                # validate request body
                body_params = request.get_json()
                try:
                    value = type_(**body_params)
                    validated[name] = value
                except ValidationError as e:
                    for err in e.errors():
                        err["loc"] = ("body", *err["loc"])
                        errors["details"].append(err)
            else:
                # validate request query params
                # get from request args or default value
                query_param = request.args.get(name, f_defaults.get(name))
                try:
                    value = parse_obj_as(type_, query_param)
                    validated[name] = value
                except ValidationError as e:
                    for err in e.errors():
                        err["loc"] = ("query", name)
                        errors["details"].append(err)

        if errors["details"]:
            return jsonify(errors), 400
        kwargs = {**kwargs, **validated}
        r = f(*args, **kwargs)
        # covert response to json
        if rsp_model:
            try:
                r = rsp_model(**r)
                return jsonify(r), status
            except ValidationError as e:
                return e.json(), 400

        return r, status

    return wrapper
