#!/usr/bin/env python

"""The setup script."""

from typing import List

from setuptools import find_packages
from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements: List[str] = []

setup_requirements: List[str] = []

test_requirements: List[str] = []

setup(
    author="Harry McPhee Winters",
    author_email="harry.mc.winters+HarrPy_author_info@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Just a PyPI mess around. Nothing to see here ;)_",
    entry_points={"console_scripts": ["harrpy=harrpy.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="harrpy",
    name="harrpy",
    packages=find_packages(include=["harrpy", "harrpy.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/harrymwinters/harrpy",
    version="0.1.0",
    zip_safe=False,
)
