# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

import typing

import pandas as pd


JsonType = typing.Any
"""
A type for a generic JSON value.
"""

Path = typing.Text
"""
An unique identifier for a time-series in the database.
"""

RawCallbackType = typing.Callable[
    [typing.Text],
    typing.Awaitable[None]
]
"""
A raw callback is an `async` function (or a `@asyncio.coroutine` decorated
function) taking as arguments a string, i.e., a line returned by the
republish interface, and calls a callback with each update.
"""

SeriesCallbackType = typing.Callable[
    [Path, pd.Series],
    typing.Awaitable[None]
]
"""
A series callback is an `async` function (or a `@asyncio.coroutine` decorated
function) taking as arguments a Path and a time-series.
"""
