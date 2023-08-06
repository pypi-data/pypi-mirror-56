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
""" Extensions and integrations.

This is just a stub for now to keep track of potential extension spots in the
code. In the future this will be a starting place for all integrations with
external libraries.
"""
import threading
from typing import Any, Optional, Tuple

from marshmallow import Schema

from apiref import exc

storage = threading.local()


def build_response(
    status_code: int,
    schema: Optional[Schema],
    raw_result: Any
) -> Any:
    """ Build response using the configured response builder.

    See:
        set_response_builder()
    """
    if not hasattr(storage, 'response_builder') or storage.response_builder is None:
        raise exc.Error("No response builder configured")

    return storage.response_builder(status_code, schema, raw_result)


def load_payload(*args: Any, **kw: Any) -> Any:
    """ Load payload from view arguments.

    When the `apiref.payload` decorator is used, this function is called to
    load the payload before parsing it and injecting into the view function. The
    *args, **kw will depend on the framework used (those should match the view
    function arguments).
    """
    global storage

    if not hasattr(storage, 'payload_loader') or storage.payload_loader is None:
        raise exc.Error("No payload loader configured")

    return storage.payload_loader(*args, **kw)


def set_response_builder(builder) -> None:
    """ Set current global response builder.

    All responses built after this call will use the given *builder* function.
    """
    storage.response_builder = builder


def set_payload_loader(payload_loader) -> None:
    """ Set payload loader for use by `apiref.payload`. """
    storage.payload_loader = payload_loader


def dummy_response_builder(
    status_code: int,
    schema: Optional[Schema],
    raw_result: Any
) -> Tuple[Any, int]:
    """ Will process the response and always return it as a tuple (response, code).
    """
    if schema:
        return schema.dump(raw_result), status_code

    return raw_result, status_code
