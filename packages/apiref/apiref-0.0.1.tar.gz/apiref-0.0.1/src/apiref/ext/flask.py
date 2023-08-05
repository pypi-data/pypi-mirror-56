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
from typing import Any, Optional

import flask
from marshmallow import Schema


def flask_response_builder(
    status_code: int,
    schema: Optional[Schema],
    raw_result: Any
):
    """ Response builder for Flask framework. """
    headers = None

    # Coerce the raw result to: data, headers, status
    if isinstance(raw_result, tuple):
        if len(raw_result) == 2:
            data, headers = raw_result
        else:
            data = raw_result
    else:
        data = raw_result

    # Use the schema to dump the data.
    if schema:
        data = schema.dump(data)

    # Create flask native response.
    response = flask.Response(
        status=status_code,
        content_type='application/json',
        headers=headers,
    )

    # Only set response data if we have any
    if data:
        response.set_data(json.dumps(data))

    return response


def _flask_payload(*args: Any, **kw: Any) -> Any:
    del args, kw  # Unused here

    return flask.request.json
