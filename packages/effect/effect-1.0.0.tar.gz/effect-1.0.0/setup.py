#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="effect",
    version="1.0.0",
    description="pure effects for Python",
    long_description=open("README.rst").read(),
    url="http://github.com/python-effect/effect/",
    author="Christopher Armstrong",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["effect"],
    install_requires=["attrs"],
)
