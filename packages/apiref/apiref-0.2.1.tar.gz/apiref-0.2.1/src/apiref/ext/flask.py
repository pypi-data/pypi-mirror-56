# Copyright 2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
""" Flask integration. """
import json
import re
from typing import Any, Callable, Dict, Iterator, Optional, Tuple

import flask
from apispec import APISpec
from marshmallow import Schema

import apiref
import apiref.ext
from apiref import types

# from flask-restplus
RE_URL = re.compile(r"<(?:[^:<>]+:)?([^<>]+)>")
Rule = Any
AnyFunc = Callable[..., Any]
JsonDict = Dict[str, Any]


def init_app(app: flask.Flask, api_spec: APISpec) -> APISpec:
    """ Load all documented urls from the api into the given spec. """
    apiref.ext.set_payload_loader(payload_loader)
    apiref.ext.set_response_builder(response_builder)

    # This is a bit hacky, but the way flask dev server works with use_reloader
    # means we cannot rely on threading locals or flask.g (the value might not
    # be initialised). Instead we will call this before every request, so that
    # we can be sure everything is configured.
    # TODO: This needs a better solution
    if app.debug and not app._got_first_request:
        @app.before_request  # nocov
        def set_payload_loader() -> None:  # pylint: disable=unused-variable
            apiref.ext.set_payload_loader(payload_loader)
            apiref.ext.set_response_builder(response_builder)

    for rule, view_fn in iter_routes(app):
        if not types.RouteMeta.has_meta(view_fn):
            print(f"-- {rule.endpoint} undocumented - skipping... ")
            continue

        add_route(api_spec, view_fn, rule, app=app)

    return api_spec


def iter_routes(app: flask.Flask) -> Iterator[Tuple[Rule, AnyFunc]]:
    """ Iterate over app routes yielding a tuple of rule and the view function. """
    for rule in app.url_map.iter_rules():
        view_fn = app.view_functions.get(rule.endpoint)
        yield rule, view_fn


def add_route(
    api_spec: APISpec,
    view_fn: AnyFunc,
    rule: Optional[Rule] = None,
    *,
    app: Optional[flask.Flask] = None
) -> None:
    """ Add new route to APISpec.

    Args:
        api_spec:
            An `APISpec` instance. The route will append the path operations
            and schemas onto this spec.
        view_fn:
            The view function we want to add to the spec.
        rule:
            Flask URL rule. If not given, the function will try to look it up
            in the flask app (``current_app`` or the one provided via *app*
            argument).
        app:
            If the rule is not given, this function will try to look it up
            in the current flask app. It can either use the *app* provided or
            ``flask.current_app``.
    """
    spec, schemas = apiref.spec_for_route(view_fn)

    if not rule:
        rule = _rule_for_view(view_fn, app)

    # Register the schemas used by the route.
    for schema in schemas:
        schema_name = apiref.schema_name(schema)

        # Only add if it's not already registered (would cause exception).
        if schema_name not in api_spec.components._schemas:
            api_spec.components.schema(schema_name, schema=schema)

    # Exclude HEAD and OPTIONS as they are auto added by flask.
    methods = list(rule.methods - {'HEAD', 'OPTIONS'})

    # If the rule is part of a blueprint, use blueprint name as tag.
    if '.' in rule.endpoint:
        blueprint_tag = rule.endpoint.split('.', 1)[0]
        spec.setdefault('tags', [blueprint_tag])

    api_spec.path(
        path=_spec_path_from_rule(rule),
        operations={
            method.lower(): spec for method in methods
        }
    )


def response_builder(
    status_code: int,
    schema: Optional[Schema],
    raw_result: Any
):
    """ Response builder for Flask framework.

    You should never need to manually set the response builder for flask. Use
    `apiref.ext.flask.init_app` instead.

    Example:

        >>> import apiref.ext
        >>> import apiref.ext.flask
        >>>
        >>> apiref.ext.set_response_builder(apiref.ext.flask.response_builder)

    """

    # Coerce the raw result to: data, headers, status
    if isinstance(raw_result, tuple) and len(raw_result) == 2:
        data, headers = raw_result
    else:
        data, headers = raw_result, None

    # Create flask native response.
    response = flask.Response(
        status=status_code,
        content_type='application/json',
        headers=headers,
    )

    # Only use schema when it's given
    if schema and data:
        data = schema.dump(data)

    # Only set response data if we have any
    if data:
        response.set_data(json.dumps(data))

    return response


def _rule_for_view(view_fn: AnyFunc, app: Optional[flask.Flask] = None) -> Rule:
    """ Return flask url map rule for the give view function. """
    if app is None:
        app = flask.current_app

    for endpoint, view in app.view_functions.items():
        if view == view_fn:
            # Support 1 route per view for now. Supporting multiple needs
            # to include rethinking add_route.
            return app.url_map._rules_by_endpoint.get(endpoint)[0]

    raise apiref.Error(f"Can't find rule for {view_fn}")


def payload_loader(*args: Any, **kw: Any) -> Any:
    """ apiref payload loader for flask.

    This will use ``flask.request.json`` to extract the payload.

    You should never need to manually set the payload loader for flask. Use
    `apiref.ext.flask.init_app` instead.

    Example:

        >>> import apiref.ext
        >>> import apiref.ext.flask
        >>>
        >>> apiref.ext.set_payload_loader(apiref.ext.flask.payload_loader)

    See:
        apiref.ext.flask.init_app

    """
    del args, kw  # Unused here

    return flask.request.json


def _spec_path_from_rule(rule: Any) -> str:
    return RE_URL.sub(r'{\1}', rule.rule)
