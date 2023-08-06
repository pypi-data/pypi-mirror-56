# -*- coding: utf-8 -*-

# Copyright (2017-2018) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
from setuptools import setup, find_packages
# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['scripts/oneview-redfish-toolkit'],
    setup_requires=["pbr"],
    download_url="https://github.com/HewlettPackard/oneview-redfish-toolkit/"
    "tarball/0.3.3",
    python_requires='>=3.5',
    pbr=True
    )
