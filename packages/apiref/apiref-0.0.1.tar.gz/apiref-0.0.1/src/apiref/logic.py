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
""" Core logic for apiref library. """
from collections import OrderedDict
from typing import Any, Dict, Set, Tuple, Union

from marshmallow import Schema

from . import types


SpecDict = Dict[Any, Any]


def spec_for_route(route_meta: types.RouteMeta) -> Tuple[SpecDict, Set[Schema]]:
    """ Take route meta and generate OpenAPI path spec. """
    spec = {}
    responses: Dict[Union[str, int], Any] = OrderedDict()
    schemas: Set[Schema] = set()   # List of all marshmallow schemas used.

    # Get response from route result.
    if route_meta.result:
        responses[route_meta.result.code] = route_meta.result.to_spec()
        if route_meta.result.schema:
            schemas.add(route_meta.result.schema)

    # Get remaining responses.
    for code, response in sorted(route_meta.responses.items(), key=lambda x: x[0]):
        responses[code] = response.to_spec()
        if response.schema:
            schemas.add(response.schema)

    # Only use responses if there are any defined.
    if responses:
        spec['responses'] = responses

    # Get the expected request body definition.
    if route_meta.payload:
        spec['payload'] = route_meta.payload.to_spec()
        if route_meta.payload.schema:
            schemas.add(route_meta.payload.schema)

    # Include summary if the function has docstring.
    if route_meta.summary:
        spec['summary'] = route_meta.summary

    # Include description if the function has one in the docstring.
    if route_meta.description:
        spec['description'] = route_meta.description

    return spec, schemas
