# vim: set tabstop=4
# setup.py
#!/usr/bin/env python3
""" setup script for assetvaluation module """

# Copyright (C) 2019 Juan Pablo Carbajal
# Copyright (C) 2019 Reza Housseini
# Copyright (C) 2019 Jeannette Lippuner
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Author: Juan Pablo Carbajal <ajuanpi+dev@gmail.com>

from os import path

from setuptools import (
    setup,
    find_packages
)

from assetvaluation import (
    __version__,
    __author__,
    __email__
)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="assetvaluation",
    packages=find_packages(),
    version=__version__,
    install_requires=["numpy>=1.17.4"],
    python_requires='>=3',
    author=__author__,
    author_email=__email__,
    url="https://kakila.wemod.info/assetvaluation",
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Other Environment",
                 "Intended Audience :: Science/Research",
                 "Intended Audience :: Financial and Insurance Industry",
                 "Intended Audience :: Other Audience",
                 "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                 "Topic :: Scientific/Engineering",
                 "Topic :: Office/Business",
                 "Topic :: Office/Business :: Financial",
                 "Topic :: Office/Business :: Financial :: Accounting",
                 ],
    description="Functions to support assets valuation (finance, accounting, and modelling)",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    project_urls={
    'Source': 'https://gitlab.wemod.ch/kakila/assetvaluation',
    'Issues': 'https://gitlab.wemod.ch/kakila/assetvaluation/issues',
    }
)
