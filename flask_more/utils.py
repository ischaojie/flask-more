from inspect import Parameter, signature
from typing import Callable, Iterable

from werkzeug.routing import Rule


def get_f_defaults(f: Callable) -> Iterable:
    """get func default params"""
    sig = signature(f)
    for k, v in sig.parameters.items():
        if v.default is not Parameter.empty:
            yield k, v.default


def get_normalize_path(rule: Rule) -> str:
    parts = []
    for is_dynamic, data in rule._trace:
        if is_dynamic:
            parts.append(f"{{{data}}}")
        else:
            parts.append(data)
    path = "".join(parts).lstrip("|")
    return path
