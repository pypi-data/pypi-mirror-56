# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2019 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Function to convert dictionaries to / from "dot notation".

"dot notation" is the term used to use a dot ``.`` to specify a path in a
dictionary, similar to what MongoDB uses. For example:

    ``abc.def.ghi`` -> Means the value of ``ghi``, which was get by the ``def``
    key, which in turn was obtained using the ``abc`` key.
"""


def dotify(adict):
    """
    Contract a dictionary to use "dot notation".

    This support both standard dict or OrderedDict, or any dict subclass.

    For example::

    .. code-block:: python3

        adict = {
            'key1': {
                'key2': {
                    'key3': 'string1',
                    'key4': 1000,
                },
            },
            'key4': {
                'key5': 'string2',
            },
        }

        contracted = dotify(adict)

    Will produce:

    .. code-block:: python3

        {
            'key1.key2.key3': 'string1',
            'key1.key2.key4': 1000,
            'key4.key5': 'string2',
        }

    :param dict adict: Original dictionary.

    :return: The contracted dictionary. Same datatype of the input.
    :rtype: dict
    """
    assert isinstance(adict, dict), 'Invalid dictionary'

    dotdict = type(adict)()

    def _dotify(anode, crumbs):
        if isinstance(anode, dict):
            for key, value in anode.items():
                _dotify(value, crumbs + [key])
            return

        dotdict['.'.join(crumbs)] = anode

    _dotify(adict, [])

    return dotdict


def undotify(dotdict):
    """
    Expand a dictionary containing keys in "dot notation".

    This support both standard dict or OrderedDict, or any dict subclass.

    For example::

    .. code-block:: python3

        dotdict = {
            'key1.key2.key3': 'string1',
            'key1.key2.key4': 1000,
            'key4.key5': 'string2',
        }

        expanded = undotify(dotdict)

    Will produce:

    .. code-block:: python3

        {
            'key1': {
                'key2': {
                    'key3': 'string1',
                    'key4': 1000,
                },
            },
            'key4': {
                'key5': 'string2',
            },
        }

    :param dict dotdict: Original dictionary containing string keys in dot
     notation.

    :return: The expanded dictionary. Same datatype of the input.
    :rtype: dict
    """
    assert isinstance(dotdict, dict), 'Invalid dictionary'

    dtype = type(dotdict)
    result = dtype()

    for key, value in dotdict.items():
        path = key.split('.')
        assert path, 'Invalid dot-notation path'

        node = result

        for part in path[:-1]:
            node = node.setdefault(part, dtype())
            assert isinstance(node, dtype), 'Incompatible paths to {}'.format(
                key,
            )

        node[path[-1]] = value

    return result


__all__ = [
    'dotify',
    'undotify',
]
