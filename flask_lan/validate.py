from inspect import signature
from typing import Any, Callable, Dict, List, Tuple

from flask import request
from pydantic import BaseModel, ValidationError, parse_obj_as

from flask_lan.utils import get_f_defaults


def validator(
    f: Callable,
    *f_args: List,
    **f_kwargs: Dict,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    errors: Dict[str, Any] = {"details": []}

    sig = signature(f)

    # all validated func params
    validated: Dict[str, Any] = {}

    # func default params
    f_defaults = dict(get_f_defaults(f))

    current_f_path_params = request.url_rule and request.url_rule.arguments

    for name, param in sig.parameters.items():
        _type = param.annotation

        # validate path params
        if current_f_path_params and name in current_f_path_params:
            try:
                value = parse_obj_as(_type, f_kwargs.get(name))
                validated[name] = value
            except ValidationError as e:
                for err in e.errors():
                    err["loc"] = ("path", name)
                    errors["details"].append(err)
        # validate request body
        elif issubclass(_type, BaseModel):
            body_params = request.get_json(force=True, silent=True)
            if body_params is None:
                body_params = request.form
            try:
                value = body_params and _type(**body_params) or _type()
                validated[name] = value
            except ValidationError as e:
                for err in e.errors():
                    err["loc"] = ("body", *err["loc"])
                    errors["details"].append(err)
        else:
            # validate request query params
            query_param = request.args.get(name, f_defaults.get(name))
            try:
                value = parse_obj_as(_type, query_param)
                validated[name] = value
            except ValidationError as e:
                for err in e.errors():
                    err["loc"] = ("query", name)
                    errors["details"].append(err)

    return errors, validated
