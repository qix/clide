#!/usr/bin/env python3

"""Clide: Helper functions for writing neat command line interfaces

Clide helps you write beautiful command line interfaces easily"""

from os import path
from setuptools import setup, find_packages

base = path.abspath(path.dirname(__file__))
with open(path.join(base, "README.rst")) as f:
    readme = f.read()

with open(path.join(base, "clide", "version.py")) as version:
    exec(version.read())

setup(
    name="clide",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license="MIT",
    description=__doc__.split("\n")[0],
    long_description=readme,
    platforms="Any",
    install_requires=["tooler", "shellby",],
    extras_require={},
    packages=find_packages(),
    entry_points={},
    scripts=[],
    test_suite="tests",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
)
