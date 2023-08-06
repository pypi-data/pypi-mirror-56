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
"""
pyXA exceptions.

The principle here is to define all pyXA specific exceptions in this
module to make them available globally.
"""


class PyXAException(Exception):
    """Base exception class for all errors raised by pyXA module."""


class FileNotFound(PyXAException):
    """Raised when the file in the path is not found."""


class PathNotFound(PyXAException):
    """Raised when the path provided by the user is not found."""
