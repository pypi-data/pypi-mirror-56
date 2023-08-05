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
""" apiref is a library for documenting API endpoints for OpenAPI spec generation.
"""
__version__ = '0.0.1'
from .decorators import (
    payload,
    response,
    result
)
from .types import (
    RouteMeta,
    RouteParam,
    RoutePayload,
    RouteResponse,
    RouteResult,
)
from .logic import *
from .exc import *
