#!/usr/bin/python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r",encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    # name="waykichain",
    name="wicc",
    version="0.0.12",
    author="louis han",
    author_email="louishwh@gmail.com",
    description="WaykiChain Wallet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louishwh/",
    packages=setuptools.find_packages(),
    install_requires=[
        'cryptos==1.36',
        'requests',
        'pbkdf2',
        'pycryptodomex',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
