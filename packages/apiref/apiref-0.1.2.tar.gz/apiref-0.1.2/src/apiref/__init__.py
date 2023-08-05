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
# pylint: disable=missing-module-docstring
__version__ = '0.1.2'
from .decorators import payload, response, result
from .types import RouteMeta
from .logic import spec_for_route
from .exc import Error

__all__ = [
    'Error',
    'payload',
    'response',
    'result',
    'spec_for_route',
    'RouteMeta',
]
