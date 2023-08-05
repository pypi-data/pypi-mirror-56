# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

import logging
import typing

import urllib.parse

from ssl import create_default_context, SSLContext

import asyncio

import aiohttp

import websockets

from ..types import JsonType, Path, RawCallbackType
from ..transport import TransportInterface


class AiohttpTransportInterface(TransportInterface):
    """
    Interface for HTTP transport layer.
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
            ) -> None:
        """
        Create a `AiohttpTransportInterface` object.

        Args:
            :param url: stanley URL.
            :type: url: str
            :param key: stanley username.
            :type: key: str
            :param key: stanley password.
            :type: key: str
            :param encoding: text encoding (utf-8 or similar).
            :type: encoding: str
            :param buffer_size: buffer size for subscriptions.
            :type: buffer_size: int
            :param max_concurrent_requests: maximum amount of concurrent requests.
            :type: max_concurrent_requests: int
            :param ca_cert: path to custom certification authority certificate.
            :type: ca_cert: str
            :param ssl_context: SSL context to enable e.g. custom certificate authorities.
            :type: ssl_context: SSLContext
        """
        super(AiohttpTransportInterface, self).__init__()
        self.logger = logging.getLogger(__name__)

        self.base_url = urllib.parse.urlparse(url).geturl()
        self.query_url = urllib.parse.urljoin(self.base_url, "/api/v1/query")
        self.post_url = urllib.parse.urljoin(self.base_url, "/api/v1/post")

        http_subscribe_url = list(urllib.parse.urlsplit(urllib.parse.urljoin(self.base_url, "/api/v1/subscribe")))
        if http_subscribe_url[0] == "https":
            http_subscribe_url[0] = "wss"
        else:
            http_subscribe_url[0] = "ws"
        self.subscribe_url = urllib.parse.urlunsplit(http_subscribe_url)
        self.logger.debug("Using websocket URI %s", self.subscribe_url)

        self.username = username
        self.password = password

        self.ssl_context = ssl_context if ssl_context is not None else create_default_context()
        if ca_cert is not None:
            self.ssl_context.load_verify_locations(ca_cert)

        self.buffer_size = buffer_size
        self.encoding = encoding
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def post_data(
                self,
                data: JsonType,
            ) -> None:
        """
        Post new data.

        :param data: data.
        :type data: str
        """

        async with self.semaphore:
            if self.username is not None and self.password is not None:
                auth = aiohttp.BasicAuth(
                    login=self.username,
                    password=self.password,
                )  # type: typing.Optional[aiohttp.BasicAuth]
            else:
                auth = None
            async with aiohttp.ClientSession(auth=auth, raise_for_status=True) as session:
                async with session.post(
                    self.post_url,
                    json=data,
                    ssl=self.ssl_context,
                ) as response:
                    self.logger.debug("Response status: %d", response.status)

    async def fetch(
                self,
                params: typing.Dict[typing.Text, typing.Text],
            ) -> typing.Text:
        """
        Fetch data by query.

        :param params: parameters.
        :type params: dict(str, str)

        :return: result.
        :rtype: JsonType
        """

        async with self.semaphore:
            self.logger.debug("Parameters: %s", params)

            async with aiohttp.ClientSession(
                conn_timeout=60,
                read_timeout=None,
                raise_for_status=True,
            ) as session:
                async with session.get(
                    self.query_url,
                    params=params,
                    timeout=None,
                    ssl=self.ssl_context,
                ) as response:
                    self.logger.debug("Response status: %d", response.status)

                    # This could easily be implemented with stream.readline(),
                    # however, that method raises an exception if a line is
                    # longer than 2**16 bytes.
                    stream = response.content
                    all_bytes = bytes()

                    while not stream.at_eof():
                        next_bytes = await stream.read(self.buffer_size)
                        all_bytes += next_bytes

                    text = all_bytes.decode(self.encoding)

                    return text

    async def subscribe(
                self,
                paths: typing.Iterable[Path],
                callback: RawCallbackType,
                ping_timeout: typing.Optional[int] = 30,
            ) -> None:
        """
        Subscribe to republish interface.

        The callback function will be called with new readings as soon as the
        archiver will republish them.

        :param paths: paths.
        :type paths: Iterable[Path]
        :param callback: callback to process new readings.
        :type callback: CallbackType
        :param ping_timeout: connection ping timeout in seconds.
            Note that, before version 1.0.0, Stanley uses a faulty websockets
            implementation and does not return correct pong messages.
            When connecting to such a server, it might be necessary to pass
            `ping_timeout=None`.
        :type ping_timeout: int
        """

        url = urllib.parse.urljoin(self.subscribe_url, "?paths={}".format(",".join(paths)))

        self.logger.debug("Subscribing to %s", url)
        connection_object = websockets.connect(
                url,
                ssl=self.ssl_context,
                ping_timeout=ping_timeout,
            )
        async with connection_object as websocket:

            while True:
                self.logger.debug("Waiting for message")
                message = await websocket.recv()
                if isinstance(message, bytes):
                    message = message.decode(self.encoding)
                await callback(message)
