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
""" types used across apiref codebase. """
from typing import Any, Callable, Dict, List, Optional, Set, TypeVar, Union

import attr
from marshmallow import Schema
from . import util


T = TypeVar('T')
AnyFunction = Callable[..., Any]
PlainType = Union[str, int, float, bool]
PlainDict = Dict[str, Union[PlainType, Dict[str, Any], List[Any]]]
Factory = Callable[..., T]


@attr.s(auto_attribs=True)
class RouteResponse:
    """ Represents route response spec. """
    schema: Optional[Schema]
    description: str

    def to_spec(self):
        """ Convert to OpenAPI spec. """
        if self.schema and self.schema.many:
            schema = {
                'type': 'array',
                'items': util.schema_name(self.schema)
            }
        else:
            schema = util.schema_name(self.schema)

        return util.dyn_dict([
            ('description', self.description),
            self.schema and ('content', {
                'application/json': {
                    'schema': schema,
                }
            })
        ])


@attr.s(auto_attribs=True)
class RouteResult(RouteResponse):
    """ Represents route result.

    This will be put i the spec as one of the responses but also used to process
    the view result.
    """
    code: int


@attr.s(auto_attribs=True)
class RouteParam:
    """ Represents route param. """
    name: str
    in_: str
    description: str = attr.ib(default='')

    def to_spec(self):
        """ Convert to OpenAPI spec. """
        return util.dyn_dict([
            ('name', self.name),
            ('in', self.in_),
            self.description and ('description', self.description),
        ])


@attr.s(auto_attribs=True)
class RoutePayload:
    """ Represents route payload.

    This defines what kind of request body is expected by the API route.
    """
    schema: Optional[Schema]
    description: str

    def to_spec(self):
        """ Convert to OpenAPI spec. """
        return util.dyn_dict([
            ('description', self.description),
            self.schema and ('content', {
                'application/json': {
                    'schema': util.schema_name(self.schema),
                }
            })
        ])


@attr.s(auto_attribs=True)
class RouteMeta:
    """ A helper class to store all the metadata about a given route. """
    view_fn: AnyFunction
    responses: Dict[int, RouteResponse] = attr.ib(default=attr.Factory(dict))
    route_params: List[RouteParam] = attr.ib(factory=list)
    result: Optional[RouteResult] = None
    payload: Optional[RoutePayload] = None
    tags: Set[str] = set()

    PARAM_NAME = '__apiref__'

    @classmethod
    def has_meta(cls, view_fn: AnyFunction) -> bool:
        """ Check if the given view_fn has any metadata attached. """
        return hasattr(view_fn, cls.PARAM_NAME)

    @property
    def summary(self):
        """ Return a summary extracted from docstring. """
        if not hasattr(self, '_summary'):
            summary, description = util.parse_docstring(self.view_fn)
            setattr(self, '_summary', summary)
            setattr(self, '_description', description)

        return self._summary

    @property
    def description(self):
        """ Return a description extracted from docstring. """
        if not hasattr(self, '_description'):
            summary, description = util.parse_docstring(self.view_fn)
            setattr(self, '_summary', summary)
            setattr(self, '_description', description)

        return self._description

    @classmethod
    def load(cls, view_fn: AnyFunction) -> 'RouteMeta':
        """ Load (or create) metadata for the given route.

        If the metadata is not yet saved on the handler, a new instance of
        `RouteMeta` will be created. You will need to save it manually in order
        for it to be persisted on the handler.
        """
        default_meta = RouteMeta(view_fn)
        return getattr(view_fn, cls.PARAM_NAME, default_meta)

    def save(self) -> None:
        """ Save route metadata into the handler it was loaded for. """
        setattr(self.view_fn, self.PARAM_NAME, self)
