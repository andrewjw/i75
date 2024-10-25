# i75
# Copyright (C) 2023 Andrew Wilkinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from glob import glob
import os
import setuptools
import sys

sys.path.insert(0, os.path.join("i75", "emulated"))

from i75 import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="i75",
    version=__version__,
    author="Andrew Wilkinson",
    author_email="andrewjwilkinson@gmail.com",
    description="A wrapper around Pimoroni's `interstate75` library which allows for running locally and easier testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewjw/i75",
    scripts=["bin/i75", "bin/i75-convert-image"],
    packages=setuptools.find_packages() + ["i75.emulated", "i75.tz", "i75.fontdata"],
    package_data={"i75": ["py.typed", "stubs/*.pyi"]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=requirements,
)
