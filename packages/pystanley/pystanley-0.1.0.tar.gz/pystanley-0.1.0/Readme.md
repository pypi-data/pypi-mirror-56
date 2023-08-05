Stanley Python Library (PyStanley)
===========

An open-source Python 3 library for interfacing to [Stanley] time-series database.
It uses the [asyncio] framework and it returns [pandas] data-frames and time-series.

https://gitlab.com/claudiomattera/pystanley/

https://gitlab.com/claudiomattera/stanley/

Copyright Claudio Mattera 2019

You are free to copy, modify, and distribute PyStanley with attribution under the terms of the MIT license. See the `License.txt` file for details.

This library originated from a similar library for interfacing to sMAP servers, developed at the Center for Energy Informatics and also available under the MIT license at <https://sdu-cfei.github.io/cfei-smap/>.
Note that pystanley is neither developed nor anyway endorsed by the Center of Energy Informatics.


Features
----

*   **Fetching historical data**.
    The user specifies a time interval and a list of paths, and the library returns all related time-series.

    The user can also request a single time-series.
    In that case, all resulting time-series will be intertwined to generate a single one.
    This is useful when time-series are split in multiple streams.

*   **Subscribing to real-time data**.
    The user specifies a list of paths and a callback, and the library will call the callback whenever a new reading is available.

    Since the library supports IO concurrency, the application can perform other operations, while waiting for new data.

*   **Posting data**.
    The users specifies a set of readings and a path.

*   **Concurrent requests**.
    The user can instantiate multiple concurrent requests to the Stanley archiver, the library (or, better, the asyncio framework) will execute them in parallel.

    A parameter defines how many concurrent requests to execute (default: 10) to not overload the archiver.
    Any further request will be transparently enqueued and executed as soon as a slot is free.

*   **Local caching**.
    Readings can be cached on the local machine.
    The library can detect when the requested time interval (or larger) is available locally.
    This saves execution time, network traffic and server load.
    If the cache does not correspond to the requested paths, it is invalidated and data is automatically fetched from the server.

    *Note*: the library cannot detect when readings are replaced/added on the server.
    Cache should be used only for immutable historical data, not for data that can change.

*   **Command line tool**.
    The tool can be used to quickly plot single time-series data, or to export them to CSV files.


Installation
----

The library can be installed using `pip`:

    pip install pystanley

In alternative, the library is also available as three different packages listed in the *tags* section:

-   Debian package, usable on Debian/Ubuntu and derivatives (anything that uses `apt`/`apt-get`).
    Install it with the following command (possibly prepended with `sudo`).

        dpkg -i /path/to/python3-pystanley_1.0.0-1_all.deb

-   Python wheel package, usable on Windows and almost every system with a Python 3 distribution.
    Install it with the following command (possibly prepended with `sudo`, or passing the `--user` option).

        pip3 install /path/to/pystanley-1.0.0-py3-none-any.whl

-   Tarball source package.
    It can be used by maintainers to generate a custom package.


Usage
----

### General Instructions

This library uses the [asyncio] framework, and returns [pandas] data-frames and time-series.

Most of the features are available as member functions of objects implementing `StanleyInterface`.
Clients should first create one of the concrete classes, e.g., `StanleyAiohttpInterface`, and then call its methods.

~~~~python
from pystanley import StanleyAiohttpInterface

...

stanley = StanleyAiohttpInterface("https://hostname.com:8443")

await stanley.fetch_readings(...)
~~~~


### Important Note about Timezones

Whenever using time-series data, proper care should be taken to correctly store and represent timezones.
Unfortunately, many tools lack support for timezones, and many users assume localtime is good enough.
This often results in issues when sharing time-series with other persons, or storing them in databases.
It also causes problems at daylight saving time changes, when the time offset of a timezone changes.
Therefore, this library enforces using timezone-aware datetimes.
Whenever a date is expected, it *must* be a timezone-aware datetime object in UTC, otherwise an exception will be generated.

This could make things more complicate and cumbersome when users are interested in localtime dynamics, such as occupancy behaviour or price trends, because they have to manually convert to and from UTC.
An example on how to convert back and forth from UTC is included in :ref:`timezones`.


### Fetching Data

To fetch data from Stanley, the caller must specify the interval as a pair of `datetime` objects and a list of paths.

~~~~python
from datetime import datetime

import pytz

from pystanley import StanleyAiohttpInterface


async def main():
    stanley = StanleyAiohttpInterface("https://hostname.com:8443")

    start = pytz.UTC.localize(datetime(2018, 1, 1, 10, 15))
    end = pytz.UTC.localize(datetime(2018, 1, 8, 4, 5))

    paths = [
        "/some/path",
        "/some/other/path",
    ]

    readings_by_path = await stanley.fetch_readings(start, end, paths)

    # It returns a dict[Path, pd.Series]

    readings = await stanley.fetch_readings_intertwined(start, end, paths)

    # It returns a single pd.Series obtained by intertwining all the results
~~~~

#### Note

If there are readings at `start` and `end` instants, the returned time-series will be defined on the *closed* interval [`start`, `end`].
Otherwise, which is a more common scenario, the returned time-series will be defined on the *open* interval ]`start`, `end`[.


### Posting Data

Users can post data (a sequence of readings, i.e., timestamp, value pairs) to any number of time-series.

~~~~python
from datetime import datetime

import pandas as pd

from pystanley import StanleyAiohttpInterface

async def main():
    series = pd.Series(...)
    path = "/some/path"

    await stanley.post_readings({
        path: series
    })
~~~~


### Subscribing to real-time data

Users can subscribe to Stanley, and be notified of every new available reading.

~~~~python
from pystanley import StanleyAiohttpInterface


async def callback(path, series):
    for timestamp, value in series.iteritems():
        print("{}: {}".format(timestamp, value))


async def main():
    stanley = StanleyAiohttpInterface("https://hostname.com:8443")

    paths = [
        "/some/path",
        "/some/other/path",
    ]

    await stanley.subscribe(paths, callback)
~~~~


### Enabling Local Cache

Pass `cache=True` to the `StanleyInterface` constructor to enable local cache.

~~~~python
from pystanley import StanleyAiohttpInterface


async def main():
    stanley = StanleyAiohttpInterface("https://hostname.com:8443", cache=True)

    # The first time data are fetched from server and cached locally.
    await stanley.fetch_readings(start, end, paths)

    # The second time they are loaded from local cache.
    await stanley.fetch_readings(start, end, paths)

    # This interval is strictly contained in the previous one, so data can
    # still be loaded from local cache.
    await stanley.fetch_readings(
        start + timedelta(days=3),
        end - timedelta(days=2),
        paths
    )

    # This interval is *NOT* strictly contained in the previous one, cache
    # will be invalidated and data will be fetched from server.
    await stanley.fetch_readings(
        start - timedelta(days=3),
        end,
        paths
    )
~~~~


### Note about *asyncio*

This library uses the *asyncio* framework.
This means that all functions and methods are actually coroutines, and they need to be called accordingly.
The caller can retrieve the event loop, and explicitly execute a coroutine

~~~~python
import asyncio

loop = asyncio.get_event_loop()

result = loop.run_until_complete(
    stanley.method(arguments)
)
~~~~

Otherwise, if the caller is itself a coroutine, it can use the corresponding syntax in Pyhton 3.5+

~~~~python
async def external_coroutine():
    result = await stanley.method(arguments)
~~~~


Command Line Utility
----

This library includes a command line utility named `pystanley`, which can be used to retrieve and plot data from a Stanley archiver.

~~~~text
usage: pystanley [-h] [-v] --url URL [--ca-cert CA_CERT] [--plot]
                 [--plot-markers] [--csv] [--start DATETIME]
                 [--end DATETIME]
                 PATH [PATH ...]

Fetch data from Stanley

positional arguments:
  PATH               Time-series path

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      increase output
  --url URL          Stanley archiver URL
  --ca-cert CA_CERT  Custom certification authority certificate
  --plot             plot results
  --plot-markers     show plot markers
  --csv              print results to stdout in CSV format
  --start DATETIME   initial time (default: 24h ago)
  --end DATETIME     final time (default: now)
~~~~

For instance, to export a single time-series to CSV file:

~~~~bash
pystanley -vv --url https://localhost.localdomain:8443/ \
    "/some/path" "/some/other/path" --start 2018-01-17T00:00:00Z \
    --csv > output.csv
~~~~


[Stanley]: https://gitlab.com/claudiomattera/stanley/

[asyncio]: https://docs.python.org/3/library/asyncio.html

[pandas]: https://pandas.pydata.org/
