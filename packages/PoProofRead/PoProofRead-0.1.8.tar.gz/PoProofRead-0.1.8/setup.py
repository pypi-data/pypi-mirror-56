#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup.py
This file is a part of PoProofRead.

Copyright (C) 2011 Kenneth Nielsen <k.nielsen81@gmail.com>

PoProofRead is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import codecs

from setuptools import setup

# from distutils.core import setup


# Shamelessly stolen from attrs
HERE = os.path.abspath(os.path.dirname(__file__))
META_PATH = os.path.join("poproofread", "__init__.py")


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


version = find_meta("version")

long_description = """\
PoProofRead is a simple application for fast and easy 
proofreading and commenting of po and podiff files"""
scripts = ["bin/poproofread-gtk"]
# The next two lines have not yet been added to the setup call
requires = ["pycairo", "PyGObject"]
provides = ["poproofread ({0})".format(version)]

data_files = [
    ("share/poproofread", ["poproofread/graphics/64.png"]),
    ("share/applications", ["poproofread.desktop"]),
    ("share/mime/packages", ["poproofread.xml"]),
]

package_data = {"poproofread": ["graphics/*", "gui/*"]}

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: X11 Applications",
    "Environment :: X11 Applications :: Gnome",
    "Environment :: X11 Applications :: GTK",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Localization",
]

setup(
    name="PoProofRead",
    version=version,
    author="Kenneth Nielsen",
    author_email="k.nielsen81@gmail.com",
    maintainer="Kenneth Nielsen",
    maintainer_email="k.nielsen81@gmail.com",
    url="https://gitlab.com/pyg3t/poproofread",
    description="PoProofRead, a po and podiff file proofreader",
    long_description=long_description,
    download_url="https://gitlab.com/pyg3t/poproofread/-/packages",
    classifiers=classifiers,
    platforms="any",
    license="GPL",
    packages=["poproofread"],
    scripts=scripts,
    install_requires=requires,
    # provides=provides,
    package_data=package_data,
    data_files=data_files,
    python_requires=">=3.6",
)
