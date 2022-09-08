import sys
from inspect import Parameter, signature
from typing import Callable

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
        if v.default is not Parameter.empty:
            yield k, v.default
