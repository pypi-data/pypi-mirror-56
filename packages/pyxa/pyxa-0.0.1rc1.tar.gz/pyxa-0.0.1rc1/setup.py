# Copyright 2019 XAMES3. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ======================================================================
"""pyXA is an open source function serving framework for Charlotte AI.

pyXA is an open source software library for high-performance complex
functional programming. Its flexible architecture allows easy deployment
of its functional usage across a variety of domains.

Originally inspired by TensorFlow & Rasa, it comes with strong support
for continuous updates, reliable functions and overall ease of use.
"""
from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup

from pyxa.utils.settings import (AUTHOR, MAINTAINER_EMAIL,
                                 PACKAGE_NAME, PACKAGE_VERSION)

DOCLINES = __doc__.split('\n')

# This package adheres to Semantic Versioning Specification (SemVer)
# starting with version 0.0.1.
VERSION = PACKAGE_VERSION

REQUIRED_PACKAGES = [
    'fuzzywuzzy',
    'geocoder',
    'geolocation-python',
    'googlemaps',
    'hurry.filesize',
    'python-Levenshtein',
    'reverse-geocode']

setup(name=PACKAGE_NAME,
      version=VERSION,
      url='https://github.com/xames3/pyxa/',
      download_url='https://github.com/xames3/pyxa/tags',
      author=AUTHOR,
      author_email='xames3.developer@gmail.com',
      maintainer=AUTHOR,
      maintainer_email=MAINTAINER_EMAIL,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
      license='Apache 2.0',
      description=DOCLINES[0],
      long_description='\n'.join(DOCLINES[2:]),
      long_description_content_type='text/plain',
      keywords='pyxa charlotte ai artificial intelligence',
      zip_safe=False,
      install_requires=REQUIRED_PACKAGES,
      python_requires='~=3.5',
      include_package_data=True,
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'pyxa = pyxa.parser:main'
            ]
        })
