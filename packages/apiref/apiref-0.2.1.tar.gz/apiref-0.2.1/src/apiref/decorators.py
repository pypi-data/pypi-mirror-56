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
""" Decorators for API routes (view functions). """
from functools import wraps
from typing import Optional

from marshmallow import Schema

from .types import (
    RouteResponse,
    RouteResult,
    RoutePayload,
    RouteMeta,
)
from . import ext


def payload(
    schema: Optional[Schema] = None,
    description: str = '',
    positional: bool = False,
    converter = None,
):
    """ Define an API route accepted payload.

    This is what is passed in the request body.

    Example:

        >>> import apiref
        >>> import apiref.ext
        >>> from marshmallow import Schema, fields
        >>>
        >>> apiref.ext.set_payload_loader(lambda *a, **kw: {'value': '123'})
        >>>
        >>> class FakeSchema(Schema):
        ...     value = fields.Str()
        >>>
        >>>
        >>> def get_payload(*args, **kw):
        ...     return {'value': '123'}
        >>>
        >>>
        >>> @apiref.payload(FakeSchema())
        ... def fake_route(payload):
        ...     return payload
        >>>
        >>>
        >>> fake_route()
        {'value': '123'}
        >>> apiref.ext.set_payload_loader(None)
    """
    def decorator(fn):  # pylint: disable=missing-docstring
        meta = RouteMeta.load(fn)
        meta.payload = RoutePayload(schema, description)
        meta.save()

        @wraps(fn)
        def wrapper(*args, **kw):
            # Parse request using the given schema
            payload_data = ext.load_payload(*args, **kw)
            payload = schema.load(payload_data)

            if converter:
                payload = converter(payload)

            # Inject the payload into the view function arguments.
            if positional:
                args = tuple([*args, payload])
            else:
                kw['payload'] = payload

            # Call the original view function.
            return fn(*args, **kw)

        return wrapper
    return decorator


def result(
    code: int = 200,
    schema: Optional[Schema] = None,
    description: str = '',
):
    """ Define the schema for the main route value.

    This will be used both to generate the OpenAPI spec as well as to marshall
    the actual function return value with the schema provided.

    Example:

        >>> import apiref
        >>> import apiref.ext
        >>> from marshmallow import Schema, fields
        >>>
        >>> apiref.ext.set_response_builder(apiref.ext.dummy_response_builder)
        >>>
        >>> class SimpleSchema(Schema):
        ...     value = fields.Str()
        >>>
        >>> @apiref.result(201, SimpleSchema())
        ... def fake_route():
        ...     return {'value': 123}
        >>>
        >>> fake_route()
        ({'value': '123'}, 201)
        >>> apiref.ext.set_response_builder(None)

    """
    def decorator(fn):  # pylint: disable=missing-docstring
        meta = RouteMeta.load(fn)
        meta.result = RouteResult(schema, description, code)
        meta.save()

        @wraps(fn)
        def wrapper(*args, **kw):
            rv = fn(*args, **kw)
            response = ext.build_response(code, schema, rv)
            return response

        return wrapper
    return decorator


def response(status, schema=None, description=''):
    """ Define a single response for the given handler.

    You can define multiple responses for the given handler by using this
    decorator multiple times.
    """
    def decorator(fn):  # pylint: disable=missing-docstring
        meta = RouteMeta.load(fn)
        meta.responses[status] = RouteResponse(schema, description)
        meta.save()
        return fn

    return decorator


def tags(*tags: str):
    """ Add tags to route reference docs. """
    def decorator(fn):
        meta = RouteMeta.load(fn)
        meta.tags = set(tags)
        meta.save()
        return fn

    return decorator
