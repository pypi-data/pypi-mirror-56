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
"""Parses command line arguments."""

import argparse
import logging
from typing import NoReturn

from pyxa.cli import strings
from pyxa.cli.arguments import add_logging_options
from pyxa.cli.commands import create
from pyxa.cli.formatter import PyXAHelpFormatter as HelpFormatter
from pyxa.utils.common import set_log_level
from pyxa.utils.settings import PACKAGE_NAME, PACKAGE_VERSION

logger = logging.getLogger(__name__)


def global_parser() -> argparse.ArgumentParser:
    """Parses arguments for pyXA module."""
    print()
    prog = PACKAGE_NAME.lower()
    usage = f'{prog} <command> [options]'
    parser = argparse.ArgumentParser(prog=prog,
                                     usage=usage,
                                     formatter_class=HelpFormatter,
                                     conflict_handler='resolve',
                                     epilog=strings.epilog)
    parser._positionals.title = 'Commands'
    parser._optionals.title = 'Extra Options'
    parser.add_argument('-h',
                        '--help',
                        action='store_true',
                        default=argparse.SUPPRESS,
                        help='Show help.')
    parser.add_argument('-V',
                        '--version',
                        action='store_true',
                        default=argparse.SUPPRESS,
                        help='Show currently installed pyXA version and exit.')

    parent_parser = argparse.ArgumentParser(add_help=True)
    add_logging_options(parent_parser)
    parent_parsers = [parent_parser]

    subparsers = parser.add_subparsers(prog=prog)
    create.subparser(subparsers, parents=parent_parsers)
    return parser


def main() -> NoReturn:
    """Runs pyXA as a standalone application."""
    parser = global_parser()
    cmd_args = parser.parse_args()

    log_level = cmd_args.loglevel if hasattr(cmd_args, 'loglevel') else None
    set_log_level(log_level)

    if hasattr(cmd_args, 'function'):
        cmd_args.function(cmd_args)
    elif hasattr(cmd_args, 'version'):
        print(f'Currently installed pyXA version is {PACKAGE_VERSION}')
    else:
        parser.print_help()
        exit(1)
