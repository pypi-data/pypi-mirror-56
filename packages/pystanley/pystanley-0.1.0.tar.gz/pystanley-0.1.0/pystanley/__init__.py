# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

from json import dumps as json_dumps
from datetime import datetime
import logging
import heapq
from hashlib import md5
from ssl import SSLContext

import pandas as pd
import typing

from .types import Path, SeriesCallbackType
from .transport import TransportInterface
from .transport.aiohttp import AiohttpTransportInterface
from .validation import parse_and_validate
from .cache import (
    load_readings_from_cache,
    save_readings_to_cache,
)


class StanleyInterface(object):
    """
    An interface to stanley time-series database.
    """

    def __init__(
                self,
                transport_interface: TransportInterface,
                cache: bool = False,
                loose_validation: bool = False,
            ) -> None:
        """
        Create a `StanleyInterface` object.

        :param transport_interface: transport interface.
        :type transport_interface: TransportInterface
        :param cache: set to True to use local cache.
        :type cache: bool
        :param cache: set to True to ignore JSON validation errors.
        :type cache: bool
        """

        super(StanleyInterface, self).__init__()

        self.logger = logging.getLogger(__name__)

        self.transport_interface = transport_interface

        self.use_local_cache = cache
        self.loose_validation = loose_validation

    async def fetch_readings(
                self,
                start: datetime,
                end: datetime,
                paths: typing.Iterable[Path],
                limit: typing.Optional[int] = None,
            ) -> typing.Dict[Path, pd.Series]:
        """
        Query for readings and return by path.

        Query stanley for all readings between `start` and `end`.
        The results are returned by path.

        :param start: start time.
        :type start: datetime
        :param end: end time.
        :type end: datetime
        :param paths: time-series paths.
        :type paths: Iterable[Path]
        :param limit: maximum number of readings (-1 for unlimited)
        :type limit: int

        :returns: A mapping path -> time-series.
        :rtype: dict(Path, pd.Series)
        """

        if self.use_local_cache:
            try:
                data = load_readings_from_cache(start, end, paths, limit)
            except Exception as exception:
                self.logger.debug("Could not load from cache: %s", str(exception))
                data = await self._fetch_readings(start, end, paths, limit)
                save_readings_to_cache(data, start, end, paths, limit)

        else:
            data = await self._fetch_readings(start, end, paths, limit)

        # Cached data might be larger than the requested period, truncate it.
        def truncate(series: pd.Series) -> pd.Series:
            series = series[series.index >= start]
            series = series[series.index <= end]
            return series

        return {
            path: truncate(series)
            for path, series in data.items()
        }

    async def fetch_readings_intertwined(
                self,
                start: datetime,
                end: datetime,
                paths: typing.Iterable[Path],
                limit: typing.Optional[int] = None,
            ) -> pd.Series:
        """
        Query for readings and return a single time-series.

        Query the stanley archiver for all readings between `start` and `end`.
        The results are intertwined to a single time-series.

        :param start: start time.
        :type start: datetime
        :param end: end time.
        :type end: datetime
        :param paths: time-series paths.
        :type paths: Iterable[Path]
        :param limit: maximum number of readings
        :type limit: int

        :returns: intertwined time-series.
        :rtype: pd.Series
        """
        results = await self.fetch_readings(start, end, paths, limit)
        return intertwine_series(results.values())

    async def post_readings(
                self,
                readings: typing.Union[typing.Dict[typing.Text, pd.Series], typing.Tuple[typing.Text, pd.Series]],
            ) -> None:
        """
        Post new readings to existing time-series.

        :param readings: either a dictionary {str: series} or a pair (str, pd.Series).
        :type readings: dict|pd.Series
        """

        if isinstance(readings, dict):
            serieses = readings  # type: typing.Dict[typing.Text, pd.Series]
        elif isinstance(readings, tuple):
            serieses = {
                readings[0]: readings[1]
            }

        payloads = [
            {
                "path": path,
                "readings": _dump_series(series),
            }
            for path, series in serieses.items()
        ]

        self.logger.debug("Payload: %s", json_dumps(payloads))

        await self.transport_interface.post_data(payloads)

    async def subscribe(
                self,
                paths: typing.Iterable[Path],
                callback: SeriesCallbackType,
                ping_timeout: int = 30
            ) -> None:
        """
        Subscribe to Stanley republish interface.
        The callback function will be called with new readings as soon as the
        archiver will republish them.

        :param paths: paths to subscribe.
        :type paths: Iterable[Path]
        :param callback: callback to process new readings.
        :type callback: SeriesCallbackType
        :param ping_timeout: connection ping timeout in seconds.
            Note that, before version 1.0.0, Stanley uses a faulty websockets
            implementation and does not return correct pong messages.
            When connecting to such a server, it might be necessary to pass
            `ping_timeout=None`.
        :type ping_timeout: int
        """

        async def raw_callback(
                    line: typing.Text
                ) -> None:
            payloads = parse_and_validate(
                line,
                "subscribe_response_schema",
                self.loose_validation
            )
            for payload in payloads:
                path = payload["path"]
                readings = payload["readings"]
                series = _parse_readings(path, readings)

                await callback(path, series)

        return await self.transport_interface.subscribe(paths, raw_callback, ping_timeout)

    async def _fetch_readings(
                self,
                start: datetime,
                end: datetime,
                paths: typing.Iterable[Path],
                limit: typing.Optional[int],
            ) -> typing.Dict[Path, pd.Series]:

        params = {
            "paths": ",".join(map(str, paths)),
            "start": str(_to_nanos_timestamp(start)),
            "end": str(_to_nanos_timestamp(end)),
        }
        if limit:
            params["limit"] = str(limit)

        output = await self.transport_interface.fetch(params)
        results = parse_and_validate(
            output,
            "select_response_schema",
            self.loose_validation
        )
        return {
            result["path"]: _parse_readings(result["path"], result["readings"])
            for result in results
        }


def _dump_series(series: pd.Series) -> typing.List[typing.List]:
    return list(map(lambda a: list(a), zip(
        [_to_nanos_timestamp(ts) for ts in series.index],
        [float(v) for v in series.values]
    )))


def _parse_readings(
        path: Path,
        readings: typing.List[typing.List]
        ) -> pd.Series:
    if len(readings) == 0:
        timestamps = []  # type: typing.List[int]
        values = []  # type: typing.List[float]
    else:
        timestamps, values = zip(*readings)

    index = pd.to_datetime(timestamps, unit="ns", utc=True)
    return pd.Series(values, index=index, name=str(path))


def _to_nanos_timestamp(date: datetime) -> int:
    if date.tzinfo is None:
        raise RuntimeError(
            "Cannot convert a timezone-naive datetime to a timestamp"
        )
    return int(10**9 * date.timestamp())


class StanleyAiohttpInterface(StanleyInterface):
    """
    An interface to stanley time-series database over HTTP.
    """

    def __init__(
                self,
                url: typing.Text,
                username: typing.Optional[typing.Text] = None,
                password: typing.Optional[typing.Text] = None,
                encoding: typing.Text = "utf-8",
                buffer_size: int = 2**16,
                max_concurrent_requests: int = 10,
                ca_cert: typing.Optional[typing.Text] = None,
                ssl_context: typing.Optional[SSLContext] = None,
                cache: bool = False,
            ) -> None:
        """
        Create a `StanleyAiohttpInterface` object.

        All arguments are passed to `pystanley.transport.AiohttpTransportInterface`.

        :param url: stanley URL.
        :type: url: str
        :param key: stanley username.
        :type: key: str
        :param key: stanley password.
        :type: key: str
        :param encoding: text encoding (utf-8 or similar).
        :type encoding: str
        :param buffer_size: buffer size for subscriptions.
        :type buffer_size: int
        :param max_concurrent_requests: maximum amount of concurrent requests.
        :type max_concurrent_requests: int
        :param ca_cert: path to custom certification authority certificate.
        :type: ca_cert: str
        :param ssl_context: SSL context to enable e.g. custom certificate authorities.
        :type: ssl_context: SSLContext
        :param cache: set to True to use local cache.
        :type cache: bool
        """
        super(StanleyAiohttpInterface, self).__init__(
            AiohttpTransportInterface(
                url,
                username,
                password,
                encoding,
                buffer_size,
                max_concurrent_requests,
                ca_cert,
                ssl_context,
            ),
            cache=cache
        )


def intertwine_series(serieses: typing.Iterable[pd.Series]) -> pd.Series:
    """
    Convert a list of time-series to a single time-series, such that readings
    are in order

    :param serieses: list of time-series.
    :type serieses: Iterable[pd.Series]

    :returns: A new intertwined time-series.
    :rtype: pd.Series
    """

    lists = [
        [
            (index, value)
            for index, value in series.iteritems()
        ]
        for series in serieses
        if len(series) > 0
    ]

    if len(lists) == 0:
        return pd.Series()

    index, values = zip(*heapq.merge(*lists))

    series = pd.Series(values, index=index)
    series = series[~series.index.duplicated(keep="first")]
    return series
