# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

from datetime import datetime
import logging
import pickle
from os.path import join
from os import makedirs
from hashlib import sha512
from base64 import b32encode

import pandas as pd
import typing

import appdirs

from .types import Path


def load_readings_from_cache(
            start: datetime,
            end: datetime,
            paths: typing.Iterable[Path],
            limit: typing.Optional[int],
        ) -> typing.Dict[typing.Text, pd.Series]:
    """
    Load readings from local cache

    Cache file name is generated from the path. If such file exists, it is
    loaded using `pickle` library. Loading fails if:

    - Data contained in cache does not cover the entire period [start, end];
    - Data contained in cache had different `limit` argument.

    :param start: start time.
    :type start: datetime
    :param end: end time.
    :type end: datetime
    :param paths: time-series paths.
    :type paths: Iterable[Path]
    :param limit: maximum number of readings
    :type limit: int

    :returns: a mapping path -> time-series.
    :rtype: dict(typing.Text, pd.Series)

    :raises RuntimeError: If cache loading failed.
    """

    logger = logging.getLogger(__name__)
    cache_file_path = _get_cache_file_path(paths)
    logger.debug("Loading data from cache file: %s", cache_file_path)
    with open(cache_file_path, "rb") as cache_file:
        entry = pickle.load(cache_file)  # typing.Dict[typing.Text, typing.Any]
    if entry["start"] > start:
        raise RuntimeError("cache starts too late")
    if entry["end"] < end:
        raise RuntimeError("cache ends too early")
    if entry["limit"] != limit:
        raise RuntimeError("cache limit mismatch")
    data = entry["data"]  # type: typing.Dict[typing.Text, typing.Any]
    return data


def save_readings_to_cache(
            data: typing.Dict[typing.Text, typing.Any],
            start: datetime,
            end: datetime,
            paths: typing.Iterable[Path],
            limit: typing.Optional[int],
        ) -> None:
    """
    Save readings to local cache

    Cache file name is generated from the path.

    :param data: readings.
    :type data: dict(typing.Text, typing.Any)
    :param start: start time.
    :type start: datetime
    :param end: end time.
    :type end: datetime
    :param paths: time-series paths.
    :type paths: Iterable[Path]
    :param limit: maximum number of readings
    :type limit: int
    """

    logger = logging.getLogger(__name__)

    entry = {
        "start": start,
        "end": end,
        "data": data,
        "limit": limit,
    }
    try:
        cache_file_path = _get_cache_file_path(paths)
        logger.debug("Saving to cache")
        cache_dir = _get_cache_dir()
        makedirs(cache_dir, exist_ok=True)
        with open(cache_file_path, "wb") as cache_file:
            pickle.dump(entry, cache_file)
    except Exception as other_exception:
        logger.warning(
            "Could not save cache: %s",
            str(other_exception)
        )


def _get_cache_dir() -> typing.Text:
    cache_dir = appdirs.user_cache_dir(
        appname="pystanley",
        appauthor="io.gitlab.claudiomattera",
    )  # type: typing.Text
    return cache_dir


def _get_cache_file_path(paths: typing.Iterable[Path]) -> typing.Text:
    text = ",".join(paths)

    cache_dir = _get_cache_dir()

    # Leave UTF-8 here, do not use configurable encoding.
    # This is used to generate the cache file name.
    hash_bytes = sha512(text.encode("utf-8")).digest()
    cache_file_name = b32encode(hash_bytes).decode("utf-8")

    cache_file_path = join(cache_dir, cache_file_name)  # type: typing.Text
    return cache_file_path
