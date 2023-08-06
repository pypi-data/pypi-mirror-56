#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "dials-data>=2.0.38",
    "Jinja2",
    "h5py",
    "mock>=3.0.5",
    "msgpack",
    "orderedset",
    "procrunner>=1.0.2",
    "psutil",
    "pytest>=4.5,<5.0",
    "pytest-mock",
    "pytest-xdist>=1.28.0",
    "scikit_learn[alldeps]<0.21",
    "scipy",
    "six",
    "tabulate",
    "tqdm==4.23.4",
]
setup_requirements = []

setup(
    author="DIALS",
    author_email="dials-support@lists.sourceforge.net",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="DIALS Dependencies",
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="dials-dependencies",
    packages=find_packages(),
    setup_requires=setup_requirements,
    url="https://github.com/dials/dials-dependencies",
    version="0.9.0",
)
