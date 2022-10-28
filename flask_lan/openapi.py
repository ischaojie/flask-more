from inspect import Parameter as InspectParameter
from inspect import signature
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from pydantic import BaseModel
from pydantic.schema import schema
from werkzeug.routing import Map, Rule

from flask_lan.schemas import (
    Components,
    Contact,
    Info,
    License,
    MediaType,
    OpenAPI,
    Operation,
    Parameter,
    ParameterInType,
    PathItem,
    Reference,
    RequestBody,
    Response,
    Schema,
    Tag,
)
from flask_lan.utils import get_normalize_path

# The route paths should been excluded when generator openapi spc
EXCLUDE_PATH = ("/docs", "/openapi.json", "/redoc")

SUPPORT_HTTP_METHOD = ("GET", "POST", "PUT", "DELETE")


def gen_openapi_spec(
    routes: Map,
    view_functions: Dict[str, Callable],
    title: str,
    version: str,
    openapi_version: str = "3.0.2",
    openapi_tags: Optional[List[Dict[str, Any]]] = None,
    description: str = "",
    terms_of_service: Optional[str] = None,
    contact: Optional[Dict[str, Union[str, Any]]] = None,
    license_info: Optional[Dict[str, Union[str, Any]]] = None,
) -> OpenAPI:
    """Generate openapi specification schema"""

    info = Info(
        title=title,
        description=description,
        version=version,
        termsOfService=terms_of_service and terms_of_service,
        contact=contact and Contact(**contact),
        license=license_info and License(**license_info),
    )

    paths_with_rules: Dict[str, Dict[str, Rule]] = {}
    for rule in routes.iter_rules():
        path = get_normalize_path(rule)
        if path in EXCLUDE_PATH:
            continue

        methods_with_rule = (
            {
                method.lower(): rule
                for method in rule.methods
                if method in SUPPORT_HTTP_METHOD
            }
            if rule.methods
            else {}
        )
        paths_with_rules.setdefault(path, methods_with_rule).update(methods_with_rule)
    paths = {
        path: make_pathitem(method_rules, view_functions)
        for path, method_rules in paths_with_rules.items()
    }

    components = Components(schemas=make_schemas(routes.iter_rules(), view_functions))

    tags = [Tag(**tag) for tag in openapi_tags if tag] if openapi_tags else None

    return OpenAPI(
        openapi=openapi_version,
        info=info,
        paths=paths,
        components=components,
        tags=tags,
    )


def make_pathitem(
    method_rules: Dict[str, Rule], view_functions: Dict[str, Callable]
) -> PathItem:
    items = {}
    for method, rule in method_rules.items():
        view_func = view_functions.get(rule.endpoint, None)
        if not view_func:
            continue
        items[method] = make_operation(rule, view_func)
    for method, rule in method_rules.items():
        view_func = view_functions.get(rule.endpoint, None)
        if view_func:
            items[method] = make_operation(rule, view_func)
    return PathItem(**items)


def make_operation(rule: Rule, view_func: Callable) -> Operation:

    sig = signature(view_func)

    api_desc = getattr(view_func, "__openapi__", {})

    # make params
    parameters: List[Parameter] = []
    request_body_content = {}
    request_body_required = False
    for name, param in sig.parameters.items():
        _type = param.annotation
        # this is path params
        if name in rule.arguments:
            parameters.append(
                Parameter(name=name, in_=ParameterInType.path, required=True)
            )
        # this is request body params
        elif issubclass(_type, BaseModel):
            request_body_content["application/json"] = MediaType(
                schema_=Reference(ref=f"#/components/schemas/{_type.__name__}")
            )
            request_body_required = True
        # this is query body
        else:
            parameters.append(
                Parameter(
                    name=name,
                    in_=ParameterInType.query,
                    required=param.default is InspectParameter.empty,
                )
            )

    if not request_body_content:
        req_body = None
    else:
        req_body = RequestBody(
            content=request_body_content, required=request_body_required
        )

    # make responses
    # sig.return_annotation
    # TODO: rsp
    responses = {"200": Response(description=api_desc.get("response_description", ""))}

    return Operation(
        tags=api_desc.get("tags", None),
        summary=api_desc.get("summary", None),
        description=api_desc.get("description", None),
        parameters=parameters or None,
        requestBody=req_body,
        responses=responses,
    )


def make_schemas(
    rules: Iterator[Rule], view_functions: Dict[str, Callable]
) -> Dict[str, Union[Schema, Reference]]:
    _schemas = []
    for rule in rules:
        view_func = view_functions.get(rule.endpoint, None)
        if not view_func:
            return {}
        sig = signature(view_func)
        for _, param in sig.parameters.items():
            _type = param.annotation
            if issubclass(_type, BaseModel):
                _schemas.append(_type)

    schemas = schema(_schemas, ref_prefix="#/components/schemas/").get("definitions", {})

    return schemas
