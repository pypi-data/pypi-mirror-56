#!/usr/bin/env python
#
# Copyright (C) 2019 Lukasz Migas
VERSION = "0.0.4"
DESCRIPTION = "SimpleParam: simplified parameters with optional type and range checking"

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

DISTNAME = "simpleparam"
MAINTAINER = "Lukasz G. Migas"
MAINTAINER_EMAIL = "lukas.migas@yahoo.com"
URL = "https://github.com/lukasz-migas/SimpleParam"
LICENSE = "Apache license 2.0"
DOWNLOAD_URL = "https://github.com/lukasz-migas/SimpleParam"

# with open("requirements.txt") as f:
#     INSTALL_REQUIRES = f.read().splitlines()

INSTALL_REQUIRES = []
PACKAGES = ["simpleparam"]

CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Natural Language :: English",
]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        classifiers=CLASSIFIERS,
        package_dir={"simpleparam": "simpleparam"},
    )
