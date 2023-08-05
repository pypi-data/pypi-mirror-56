#!/usr/bin/env python3

# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT


from datetime import datetime, timedelta
import argparse
import logging
import asyncio
import typing
import sys

import iso8601

from aiohttp.client_exceptions import ClientError

from pystanley import StanleyAiohttpInterface


def main() -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_main())
    finally:
        loop.close()


async def async_main() -> None:
    arguments = parse_arguments()
    setup_logging(arguments.verbose)
    logger = logging.getLogger(__name__)

    logger.debug("Using Stanley server %s", arguments.url)
    stanley = StanleyAiohttpInterface(
        arguments.url,
        ca_cert=arguments.ca_cert,
    )

    logger.debug(
        "Requesting data between %s and %s",
        arguments.start,
        arguments.end,
    )
    try:
        readings_dict = await stanley.fetch_readings(
            arguments.start,
            arguments.end,
            arguments.path,
        )

        logger.debug(
            "Fetched readings for %d time-series",
            len(readings_dict),
        )

        for path, readings in readings_dict.items():
            logger.debug(
                " Time-series %s contains %d readings from %s to %s",
                path,
                len(readings),
                readings.index[0],
                readings.index[-1],
            )

            if arguments.csv:
                print(readings.to_csv())

        if arguments.plot:
            try:
                import matplotlib.pyplot as plt

                from pandas.plotting import register_matplotlib_converters

                register_matplotlib_converters()

                figure, ax = plt.subplots()
                marker = "." if arguments.plot_markers else None
                for path, readings in readings_dict.items():
                    ax.step(
                        readings.index,
                        readings.values,
                        where="post",
                        marker=marker,
                        label=path,
                    )

                plt.show()

            except ModuleNotFoundError:
                logger.error("Matplotlib not installed")
                sys.exit(1)

    except ClientError as e:
        logger.error("%s", e)
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch data from Stanley"
    )

    now = datetime.utcnow().replace(tzinfo=iso8601.UTC)
    default_end = now
    default_start = now - timedelta(days=1)

    parser.add_argument(
        "path",
        metavar="PATH",
        type=str,
        nargs="+",
        help="Time-series path"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        help="increase output"
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Stanley archiver URL"
    )
    parser.add_argument(
        "--ca-cert",
        type=str,
        help="Custom certification authority certificate"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        default=False,
        help="plot results"
    )
    parser.add_argument(
        "--plot-markers",
        action="store_true",
        default=False,
        help="show plot markers"
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        default=False,
        help="print results to stdout in CSV format"
    )
    parser.add_argument(
        "--start",
        metavar="DATETIME",
        default=default_start,
        type=parse_datetime,
        help="initial time (default: 24h ago)"
    )
    parser.add_argument(
        "--end",
        metavar="DATETIME",
        default=default_end,
        type=parse_datetime,
        help="final time (default: now)"
    )

    return parser.parse_args()


def parse_datetime(text: typing.Text) -> datetime:
    dt = iso8601.parse_date(text)  # type: datetime
    return dt


def setup_logging(verbose: typing.Optional[int]) -> None:
    if verbose is None or verbose <= 0:
        level = logging.WARN
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(level=level)


if __name__ == "__main__":
    main()
