#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# setup.py file is part of USBdev.

# Copyright 2015-2019 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# USBdev is a tool recognition of USB devices.

# https://gitlab.com/dslackw/USBdev

# USBdev is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from USBdev.__metadata__ import (
    __prog__,
    __version__,
    __author__,
    __email__,
    __website__,
    __lib_path__
)

REQUIREMENTS = [
    "pyusb >= 1.0.0"
]

if not os.path.exists(__lib_path__):
    os.mkdir(__lib_path__)

data = [
    (__lib_path__, ["usb.ids"])
]

setup(
    name=__prog__,
    packages=["USBdev"],
    scripts=["bin/usbdev"],
    version=__version__,
    description="USBdev is a tool recognition of USB devices",
    long_description=open("README.rst").read(),
    keywords=["usb", "device"],
    author=__author__,
    author_email=__email__,
    url=__website__,
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    data_files=data,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later "
        "(GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3"],
    python_requires=">=3.7"
)
