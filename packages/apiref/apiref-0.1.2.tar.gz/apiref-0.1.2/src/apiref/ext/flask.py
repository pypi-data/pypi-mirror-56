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
from typing import Any, Dict, Optional

import flask
from marshmallow import Schema

JsonDict = Dict[str, Any]


def response_builder(
    status_code: int,
    schema: Optional[Schema],
    raw_result: Any
):
    """ Response builder for Flask framework.


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


def payload_loader(*args: Any, **kw: Any) -> Any:
    """ apiref payload loader for flask.

    This will use ``flask.request.json`` to extract the payload.

    Example:

        >>> import apiref.ext
        >>> import apiref.ext.flask
        >>>
        >>> apiref.ext.set_payload_loader(apiref.ext.flask.payload_loader)

    """
    del args, kw  # Unused here

    return flask.request.json
