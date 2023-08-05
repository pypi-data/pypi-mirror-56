#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0

""" setuptools script for packaging ua_spoofer. """

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

pkg_name = "ua_spoofer"

setup(
    name=pkg_name,
    version="1.0",
    author="Oliver Galvin",
    author_email="odg@riseup.com",
    description="A module for collecting and providing popular user agent "
                "strings, with a requests session which rotates user agents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://gitlab.com/odg/" + pkg_name,
    packages=find_packages(),
    py_modules=[pkg_name],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="user agent string spoofer spoofing random scraping crawling crawler bot",
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    python_requires=">=3",
)
