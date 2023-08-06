# flake8: noqa

# This file is part of modelbase.
#
# modelbase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# modelbase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with modelbase.  If not, see <http://www.gnu.org/licenses/>.

import sys
import setuptools
import pathlib
import os
import codecs
import re
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


README = (pathlib.Path(__file__).parent / "README.md").read_text()

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="modelbase",
    version=find_version("modelbase", "__init__.py"),
    description="A package to build metabolic models",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ebenhoeh/modelbase",
    author="Oliver Ebenhoeh",
    author_email="oliver.ebenhoeh@hhu.de",
    license="GPL3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="modelling ode pde metabolic",
    project_urls={
        "Documentation": "https://modelbase.readthedocs.io/en/latest/",
        "Source": "https://gitlab.com/ebenhoeh/modelbase",
        "Tracker": "https://gitlab.com/ebenhoeh/modelbase/issues",
    },
    packages=find_packages("."),
    install_requires=[
        "numpy>=1.16",
        "scipy",
        "matplotlib>=3.0.3",
        "pandas",
        "python-libsbml",
    ],
    python_requires=">3.5.0",
    zip_safe=False,
)
