#!/usr/bin/env python3
#
# Copyright 2019 Tymoteusz Blazejczyk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup the ReCoVer package."""

import pathlib
import setuptools

TOPIC_ENGINEERING = 'Topic :: Scientific/Engineering :: '


def readme() -> str:
    """Load the README file content."""
    text = str()
    with pathlib.Path('README.md').open() as readme_file:
        text = readme_file.read()
    return text


setuptools.setup(
    name='recover',
    version='v0.0.0',
    description=(
        'An effective Remote Co-Verification (ReCoVer) library of '
        'hardware and software co-designs'
    ),
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/tymonx/recover',
    author='Tymoteusz Blazejczyk',
    author_email='tymoteusz.blazejczyk.pl@gmail.com',
    license='Apache 2.0',
    keywords=[
        'co-verification',
        'systemverilog',
        'verification',
        'co-designs',
        'hardware',
        'verilog',
        'vhdl',
        'fpga',
        'vpi',
        'hdl',
        'rtl',
        'hw',
        'sw'
    ],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        TOPIC_ENGINEERING + 'Electronic Design Automation (EDA)',
        TOPIC_ENGINEERING + 'Interface Engine/Protocol Translator'
    ]
)
