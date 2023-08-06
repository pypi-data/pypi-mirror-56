#!/usr/bin/env python

from pathlib import Path

from setuptools import find_packages, setup

THIS_DIR = Path(__file__).parent

with open(THIS_DIR.joinpath("README.md")) as readme:
    desc = readme.read()

setup(
    name="quality-viewer",
    version="0.0.3",
    url="https://github.com/DaMouse404/quality-viewer",
    packages=find_packages(include=["quality_viewer", "quality_viewer.*"]),
    author="Chris Sidebottom",
    author_email="chris@damouse.co.uk",
    description="A simple CLI for rendering Quality Views",
    long_description=desc,
    long_description_content_type="text/markdown",
    install_requires=["graphviz==0.13.2"],
    platforms="any",
    scripts=["bin/quality-viewer"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ]
)
