#!/usr/bin/python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # name="waykichain",
    name="wicc",
    version="0.0.3",
    author="louis han",
    author_email="louishwh@gmail.com",
    description="WaykiChain Wallet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louishwh/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
