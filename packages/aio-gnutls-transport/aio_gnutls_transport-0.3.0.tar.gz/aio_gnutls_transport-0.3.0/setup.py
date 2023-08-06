#!/usr/bin/python3

import sys

from setuptools import setup, findall

tests_requires = ["nose2"]

if sys.version_info[:2] < (3,7):
    tests_requires += ["async-generator"]

setup(
    name        = "aio_gnutls_transport",
    version     = "0.3.0",
    author      = "Anthony Baire",
    author_email= "Anthony.Baire@irisa.fr",
    url         = "https://gitlab.inria.fr/abaire/aio_gnutls_transport/",
    license     = "LGPL2.1+",
    description = "asyncio transport over GnuTLS",
    long_description = open("README.md").read(),
    long_description_content_type='text/markdown',
    keywords    = ["asyncio", "TLS", "transport", "GnuTLS"],

    platforms   = ["linux"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security :: Cryptography",
        ],

    packages    = ["aio_gnutls_transport"],
    cffi_modules= ["aio_gnutls_transport/_gnutls_build.py:ffibuilder"],

    data_files = [(".", ["CHANGELOG.md"])],

    setup_requires   = ["cffi>=1.0.0"],
    install_requires = ["cffi>=1.0.0"],

    tests_require = tests_requires,
)

