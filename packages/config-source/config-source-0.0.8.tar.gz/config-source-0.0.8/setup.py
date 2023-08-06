# Copyright 2019 Luddite Labs Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os.path as op
from setuptools import setup, find_packages

PY2 = sys.version_info[0] == 2
THIS_DIR = op.dirname(__file__)


def get_version():
    with open(op.join(THIS_DIR, 'src/config_source.py')) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def read(filename):
    return open(op.join(THIS_DIR, filename)).read()


tests_require = ['pytest', 'pytest-cov']

if PY2:
    tests_require += ['mock']


setup(
    name='config-source',
    version=get_version(),
    description='Simple configurations management for applications.',
    long_description=read('README.rst'),
    author='Sergey Kozlov',
    author_email='dev@ludditelabs.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=['config_source'],
    install_requires=['future>=0.16.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],

    setup_requires=['pytest-runner'],
    tests_require=tests_require
)
