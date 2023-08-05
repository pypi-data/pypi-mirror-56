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
"""Create project subparser command."""

import argparse
import os
import subprocess
from typing import List, NoReturn, Optional, Text

from pyxa.cli.commands.strings import (create_usage, create_help,
                                       create_description, project_usage,
                                       project_help, project_description,
                                       profile_usage, profile_help,
                                       profile_description, venv_usage,
                                       venv_help, venv_description)
from pyxa.cli.options import (create_args,
                              create_profile_args,
                              create_project_args,
                              create_venv_args)
from pyxa.parser import PyXAHelpFormatter as Formatter
from pyxa.utils.exceptions import PathNotFound
from pyxa.utils.settings import PACKAGE_NAME
from pyxa.utils.user import add_details_to_file, navigate_to_file

prog = PACKAGE_NAME.lower()


def subparser(subparsers: argparse._SubParsersAction,
              parents: List[argparse.ArgumentParser]) -> NoReturn:
    """Creates `create` subparser object."""
    title = os.path.basename(__file__).split('.')[0].capitalize()

    parser = subparsers.add_parser('create',
                                   usage=create_usage,
                                   help=create_help,
                                   formatter_class=Formatter,
                                   parents=parents,
                                   description=create_description,
                                   conflict_handler='resolve')
    create_args(parser)

    parser._positionals.title = f'{title} Options'
    parser._optionals.title = f'{title} Arguments'

    create = parser.add_subparsers()

    create_project_parser = create.add_parser('project',
                                              usage=project_usage,
                                              help=project_help,
                                              formatter_class=Formatter,
                                              parents=parents,
                                              description=project_description,
                                              conflict_handler='resolve')
    create_project_parser.set_defaults(function=create_project)
    create_project_parser._positionals.title = f'{title} Project Options'
    create_project_parser._optionals.title = f'{title} Project Arguments'

    create_profile_parser = create.add_parser('profile',
                                              usage=profile_usage,
                                              help=profile_help,
                                              formatter_class=Formatter,
                                              parents=parents,
                                              description=profile_description,
                                              conflict_handler='resolve')
    create_profile_parser.set_defaults(function=create_profile)
    create_profile_parser._positionals.title = f'{title} Profile Options'
    create_profile_parser._optionals.title = f'{title} Profile Arguments'

    create_venv_parser = create.add_parser('venv',
                                           usage=venv_usage,
                                           help=venv_help,
                                           formatter_class=Formatter,
                                           parents=parents,
                                           description=venv_description,
                                           conflict_handler='resolve')
    create_venv_parser.set_defaults(function=create_venv)
    create_venv_parser._positionals.title = f'{title} VirtualEnv Options'
    create_venv_parser._optionals.title = f'{title} VirtualEnv Arguments'

    parser.set_defaults(function=create_complete)
    create_project_args(create_project_parser)
    create_profile_args(create_profile_parser)
    create_venv_args(create_venv_parser)


def create_complete(args: argparse.Namespace,
                    name: Optional[Text] = None,
                    path: Optional[Text] = None,
                    project_path: Optional[Text] = None,
                    venv_name: Optional[Text] = None,
                    socket_port: Optional[int] = None):
    """Creates complete project structure."""
    name = name or args.name
    path = path or args.path
    socket_port = socket_port or args.socket_port
    venv_name = venv_name or args.venv_name

    project_path = os.path.join(path, name).replace('\\', '/')

    create_project(args, name, path)
    create_profile(args, name, project_path)
    create_venv(args, name, project_path, venv_name)


def create_project(args: argparse.Namespace,
                   name: Optional[Text] = None,
                   path: Optional[Text] = None):
    """Creates project directory."""
    from pkg_resources import resource_filename
    from distutils.dir_util import copy_tree

    name = name or args.name
    path = path or args.path

    if path == 'Current directory':
        path = os.getcwd()

    path = os.path.join(path, name).replace('\\', '/')
    copy_tree(resource_filename(__name__, 'project_template'), path)
    print(f'Creating project structure in "{path}".')


def create_profile(args: argparse.Namespace,
                   name: Optional[Text] = None,
                   project_path: Optional[Text] = None):
    """Creates user profile."""
    name = name or args.name
    project_path = project_path or args.project_path

    if project_path == 'Current directory':
        project_path = os.getcwd()

    navigate_to_file(project_path)
    add_details_to_file(project_path)

    project_path.replace('\\', '/')

    print(f'Created profile under "{project_path}/user/" folder.')


def create_venv(args: argparse.Namespace,
                name: Optional[Text] = None,
                project_path: Optional[Text] = None,
                venv_name: Optional[Text] = None):
    """Creates virtual environment."""
    name = name or args.name
    project_path = project_path or args.project_path
    venv_name = venv_name or args.venv_name

    if project_path == 'Current directory':
        project_path = os.getcwd()
    if not os.path.exists(project_path):
        raise PathNotFound
    else:
        print('Creating virtual environment...')
        subprocess.call(f'virtualenv {project_path}/{venv_name}')
