#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["fenics==2018.1.0", "Click", "numpy", "matplotlib", "munch", "scipy", "xlrd", "sympy"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

try:
    if os.environ.get("CI_COMMIT_TAG"):
        version = os.environ["CI_COMMIT_TAG"]
    else:
        version = os.environ["CI_JOB_ID"]
except KeyError:
    version = "v0.0.1"

setup(
    author="Christopher Macklen",
    author_email="cmacklen@uccs.edu",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="Mountain Lion Continuum-Scale Lithium-Ion Cell Simulator uses FEniCS to solve partial differential "
    "equations for the internal states of Lithium-Ion cells.",
    entry_points={"console_scripts": ["mtnlion=mtnlion.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="mtnlion",
    name="mtnlion",
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://gitlab.com/macklenc/mtnlion",
    version=version,
    zip_safe=False,
    python_requires=">=3.6",
)
