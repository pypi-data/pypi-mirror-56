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
"""Custom Usage, MetaVar, Help & Description Formatter."""

import argparse
import os
import textwrap


class PyXAHelpFormatter(argparse.RawTextHelpFormatter):
    """Captilizes the usage text."""

    # You can find the reference code here:
    # https://stackoverflow.com/questions/35847084/customize-argparse-help-message
    def add_usage(self, usage, actions, groups, prefix=None):

        if prefix is None:
            prefix = 'Usage: ' + '\n' + '  '

        return super(PyXAHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

    # You can find the reference code here:
    # https://stackoverflow.com/questions/35917547/python-argparse-rawtexthelpformatter-with-line-wrap
    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return textwrap.wrap(text, (os.get_terminal_size().columns / 1.3))

    # You can find the reference code here:
    # https://stackoverflow.com/questions/13423540/argparse-subparser-hide-metavar-in-command-listing
    def _format_action(self, action):
        parts = super(argparse.RawTextHelpFormatter,
                      self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = '\n'.join(parts.split('\n')[1:])
        return parts
