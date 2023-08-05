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
""" Generic utilities.

This code should not depend on the rest of the apiref codebase.
"""
import textwrap
import re
from typing import Any, Optional, Tuple

from marshmallow import Schema


def parse_docstring(obj: Any) -> Tuple[Optional[str], Optional[str]]:
    """ Extract summary and description from docstring.

    Beginning of docstring is the summary, separated from description by an
    empty line.
    """
    if obj.__doc__ is None:
        return None, None

    docstring = obj.__doc__.strip()
    parts = re.split(r'\n\s*\n', docstring, 1)
    summary = parts[0]
    description: Optional[str]

    if len(parts) == 2:
        description = textwrap.dedent(parts[1])
    else:
        description = None

    return summary, description


def dyn_dict(values):
    """ Conditionally create a dictionary.

    This function makes it possible to dynamically include and exclude fields
    from a new dictionary.

    Examples:

        >>> include_name = True
        >>>
        >>> dyn_dict([
        ...     include_name and ('name', 'John'),
        ...     ('age', 32)
        ... ])
        {'name': 'John', 'age': 32}

        >>> include_name = False
        >>> dyn_dict([
        ...     include_name and ('name', 'John'),
        ...     ('age', 32)
        ... ])
        {'age': 32}

    """
    # Filter out all falsy values - they are not tuples and should be omitted.
    return dict(v for v in values if v)


def schema_name(schema: Schema) -> str:
    """ Return schema name from schema class. """
    return schema.__class__.__name__
