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
"""Passing arguments."""

from __future__ import absolute_import

import argparse
import logging
from typing import Optional, Text, Union

from pyxa.utils.settings import (AI_NAME,
                                 NAUGHTY_HOST_PORT,
                                 VIRTUALENV_NAME)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def pass_project_name_arg(parser: Union[argparse.ArgumentParser,
                                        argparse._ActionsContainer],
                          help: Text,
                          default: Optional[Text] = AI_NAME.lower()):
    """Argument for adding the project name."""
    parser.add_argument('--name', default=default,
                        help=help, type=str, metavar='<name>')


def pass_project_path_arg(parser: Union[argparse.ArgumentParser,
                                        argparse._ActionsContainer],
                          help: Text,
                          default: Optional[Text] = 'Current directory'):
    """Argument for adding the project path."""
    parser.add_argument('--path', default=default,
                        help=help, type=str, metavar='<path>')


def pass_existing_project_path_arg(parser: Union[argparse.ArgumentParser,
                                                 argparse._ActionsContainer],
                                   help: Text):
    """Argument for adding the existing project path."""
    parser.add_argument('--project-path', help=help,
                        type=str, metavar='<path>')


def pass_venv_name_arg(parser: Union[argparse.ArgumentParser,
                                     argparse._ActionsContainer],
                       help: Text,
                       default: Optional[Text] = VIRTUALENV_NAME):
    """Argument for creating virtual environment in the project."""
    parser.add_argument('--venv-name', default=default,
                        help=help, type=str, metavar='<name>')


def pass_socket_port_arg(parser: Union[argparse.ArgumentParser,
                                       argparse._ActionsContainer],
                         help: Text,
                         default: Optional[int] = NAUGHTY_HOST_PORT):
    """Argument for SocketIO port."""
    parser.add_argument('--socket-port', default=default,
                        help=help, type=int, metavar='<port>')


def add_logging_options(parser: argparse.ArgumentParser):
    """Adds logging options to the parser object."""
    parser = parser.add_argument_group('Logging Options')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_const',
                        dest='loglevel',
                        help='Give more output. Increase output verbosity.',
                        const=logging.INFO)
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='loglevel',
                        help='Print all debugging statements.',
                        const=logging.DEBUG)
    parser.add_argument('-q',
                        '--quiet',
                        action='store_const',
                        dest='loglevel',
                        help=('Give less output. Decrease output verbosity '
                              '(respond only to WARNING, ERROR, and CRITICAL '
                              'logging levels).'),
                        const=logging.WARNING)
