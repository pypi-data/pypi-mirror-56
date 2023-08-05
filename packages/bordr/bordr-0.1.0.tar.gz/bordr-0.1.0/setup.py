#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

from pathlib import Path
import setuptools
from pkg_resources import parse_version
import re

assert parse_version(setuptools.__version__) >= parse_version("38.6.0")


def get_version(prop, project):
    project = Path(__file__).parent / project / "__init__.py"
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), project.read_text()
    )
    return result.group(1)


def read(fname):
    p = Path(__file__).parent / fname
    with p.open(encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="bordr",
    version=get_version("__version__", "bordr"),  # edit version in pybo/__init__.py
    author="Dat Quoc Nguyen",
    author_email="dqnguyen@unimelb.edu.au",
    description="A  fast and accurate POS and morphological tagging toolkit, lightly adapted to Tibetan language.",
    license="GNU General Public License",
    keywords="part-of-speech-tagger java nlp pos-tagging pos-tagger python3",
    url="https://github.com/Esukhia/RDRPOSTagger",
    packages=setuptools.find_packages(),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/Esukhia/RDRPOSTagger",
        "Tracker": "https://github.com/Esukhia/RDRPOSTagger/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Tibetan",
    ],
    package_data={},
    python_requires=">=3.6",
    dependency_links=[],
    install_requires=[],
)
