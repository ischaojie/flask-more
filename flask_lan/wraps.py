from enum import Enum
from functools import partial, wraps
from typing import Any, Callable, Dict, List, Optional, Union

from flask import jsonify
from pydantic import BaseModel

from flask_lan.validate import validator


def api(
    f: Optional[Callable] = None,
    *,
    rsp_model: Optional[BaseModel] = None,
    status: int = 200,
    tags: Optional[List[Union[str, Enum]]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
) -> Any:
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
    def wrapper(*args: List, **kwargs: Dict) -> Any:

        errors, validated = validator(f, *args, **kwargs)  # type: ignore
        if errors["details"]:
            return jsonify(errors), 400

        kwargs = {**kwargs, **validated}

        r = f(*args, **kwargs)  # type: ignore

        return r, status

    return wrapper
