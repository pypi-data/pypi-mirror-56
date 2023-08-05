#!/usr/bin/env python

# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

import sys

from setuptools import setup

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setup(
    name="pystanley",
    version="0.1.0",
    description="Interface to Stanley time-series database",
    long_description=open("Readme.md").read(),
    long_description_content_type="text/markdown",
    author="Claudio Giovanni Mattera",
    author_email="claudio@mattera.it",
    url="https://gitlab.com/claudiomattera/pystanley/",
    license="MIT",
    packages=[
        "pystanley",
        "pystanley.transport",
    ],
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "pystanley = pystanley.__main__:main",
        ],
    },
    install_requires=[
        "pandas",
        "aiohttp",
        "websockets",
        "appdirs",
        "jsonschema",
        "iso8601",
    ],
    extras_require={
        "plot":  [
            "matplotlib"
        ],
    },
    setup_requires=pytest_runner,
    tests_require=["pytest"],
)
