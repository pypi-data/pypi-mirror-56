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
"""Optional arguments for commands."""

import argparse

from pyxa.cli.arguments import (pass_existing_project_path_arg,
                                pass_project_name_arg,
                                pass_project_path_arg,
                                pass_socket_port_arg,
                                pass_venv_name_arg)


def create_args(parser: argparse.ArgumentParser):
    """Parses arguments for `create` command."""
    pass_project_name_arg(parser, help='Name of the application or project.')
    pass_project_path_arg(parser, help='Path to the project directory.')
    pass_venv_name_arg(parser, help='Name of the virtual environment.')
    pass_socket_port_arg(parser, help=('SocketIO port number, or '
                                       'http://localhost:<port>.'))


def create_project_args(parser: argparse.ArgumentParser):
    """Parses arguments for `create project` command."""
    pass_project_name_arg(parser, help='Name of the application or project.')
    pass_project_path_arg(parser, help='Path to the project directory.')


def create_profile_args(parser: argparse.ArgumentParser):
    """Parses argument for `create profile` command."""
    pass_existing_project_path_arg(parser, help=('Path where the project '
                                                 'already exists.'))


def create_venv_args(parser: argparse.ArgumentParser):
    """Parses argument for `create venv` command."""
    pass_venv_name_arg(parser, help='Name of the virtual environment.')
    pass_existing_project_path_arg(parser, help=('Path where the project '
                                                 'already exists.'))
