from enum import Enum
from functools import partial, wraps
from typing import Callable, List, Optional, Union

from flask import jsonify
from pydantic import ValidationError

from flask_lan.validate import validator


def api(
    f: Optional[Callable] = None,
    *,
    rsp_model=None,
    status: int = 200,
    tags: Optional[List[Union[str, Enum]]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
):
    if f is None:
        return partial(
            api,
            rsp_model=rsp_model,
            status=status,
            tags=tags,
            summary=summary,
            description=description,
            response_description=response_description,
        )

    api_desc = {
        "tags": tags,
        "summary": summary,
        "description": description,
        "response_description": response_description,
    }
    setattr(f, "__openapi__", api_desc)

    @wraps(f)
    def wrapper(*args, **kwargs):

        errors, validated = validator(f, *args, **kwargs)
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
