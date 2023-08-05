#!/usr/bin/env python

import os
import re
from setuptools import setup

DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

README = open(rel("README.rst")).read()
MAIN = open(rel("ldif.py")).read()
VERSION = re.search('__version__ = "([^"]+)"', MAIN).group(1)
NAME = re.search('^"""(.*) - (.*)"""', MAIN).group(1)
DESCRIPTION = re.search('^"""(.*) - (.*)"""', MAIN).group(2)


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    url="https://github.com/abilian/ldif",
    author="Abilian SAS",
    author_email="dev@abilian.com",
    py_modules=["ldif"],
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration :: "
        "Authentication/Directory :: LDAP",
    ],
)
