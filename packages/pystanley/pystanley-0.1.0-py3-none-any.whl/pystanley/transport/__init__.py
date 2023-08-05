# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

import typing

from ..types import JsonType, Path, RawCallbackType


class TransportInterface(object):
    """
    Interface for transport layer.
    """

    def __init__(self) -> None:
        super(TransportInterface, self).__init__()

    async def fetch(
                self,
                params: typing.Dict[typing.Text, typing.Text],
            ) -> typing.Text:
        """
        Fetch data by path.

        :param params: parameters.
        :type params: dict(str, str)

        :return: result.
        :rtype: typing.Text
        """
        raise RuntimeError("Not implemented")

    async def post_data(
                self,
                data: JsonType,
            ) -> None:
        """
        Post new data.

        :param data: data.
        :type data: str
        """
        raise RuntimeError("Not implemented")

    async def subscribe(
                self,
                paths: typing.Iterable[Path],
                callback: RawCallbackType,
                ping_timeout: typing.Optional[int] = 30
            ) -> None:
        """
        Subscribe to republish interface.
        The callback function will be called with new readings as soon as the
        archiver will republish them.

        :param where: paths.
        :type where: Iterable[Path]
        :param callback: callback to process new readings.
        :type callback: CallbackType
        :param ping_timeout: connection ping timeout in seconds.
        :type ping_timeout: int
        """
        raise RuntimeError('Not implemented')
