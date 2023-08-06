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
"""Usage, help and descriptions for parsers & subparsers."""

# Parent parser object.
epilog = ('For specific information about a particular command, run "pyxa '
          '<command> -h".\nRead complete documentation at: '
          '<https://github.com/xames3/pyxa>\n\nCopyright 2019 XAMES3. '
          'All Rights Reserved.')

# Create subparser object.
create_usage = ('pyxa create [options] --name <project name> --path <local '
                'project path> ...\n  '
                'pyxa create [options] project --name <project name> ...\n  '
                'pyxa create [options] profile --project-path <existing '
                'project path> ...\n  '
                'pyxa create [options] venv --venv-name <virtualenv '
                'name> ...\n  '
                'pyxa create [options] <no arguments> ...')
create_help = ('Create project directory structure for the given project '
               'name in the current directory or optionally in the given '
               'directory to unpack the necessary dependencies into it and '
               'build it further. Note that it will unpack everything in '
               '"~/.charlotte/" folder if no name is specified for the '
               'project.')
create_description = ('Description:\n  Getting started for Charlotte:\n\n  '
                      '- Creates your Charlotte AI project structure.\n  '
                      '- Creates local user profile.\n  '
                      '- Creates virtual environment if necessary.\n\n  '
                      'Although everything is configured at the beginning, '
                      'you can change and update things as per your needs.')

# Create project subparser object.
project_usage = ('pyxa create project --name <project name> --path '
                 '<local project path> ...\n  '
                 'pyxa create project --path <local project path> ...\n  '
                 'pyxa create project <no arguments> ...')
project_help = ('Create project directory structure for the given project '
                'name in the current directory or optionally in the given '
                'directory to unpack the necessary dependencies into it. '
                'Note that it will unpack everything in "~/.charlotte/" '
                'folder if no name is specified for the project (similar '
                'to the "pyxa create" except it won\'t create the profile).')
project_description = ('Description:\n  Similar to "pyxa create":\n\n  '
                       '- Creates your Charlotte AI project structure.\n  '
                       '- Doesn\'t creates local user profile though.\n\n  '
                       'Although everything is configured at the beginning, '
                       'you can change and update things as per your needs.')

# Create profile subparser object.
profile_usage = ('pyxa create profile --project-path '
                 '<existing project path> ...')
profile_help = ('Create user profile in the existing project directory. This '
                'profile is created at default path, "~/.<project directory>/'
                'user/". Generally you will need to specify "--project-path" '
                'when using this option.')
profile_description = ('Description:\n  Creates user profile:\n\n  '
                       '- Creates the local user profile in easy-to-deal '
                       '"yaml" format.\n  '
                       '- This profile hosts bunch of user specific values '
                       'which are used while building your project.\n  '
                       '- These config values can be changed later.\n  '
                       '- Existing profile will be overwritten.')

# Create virtual subparser object.
venv_usage = ('pyxa create venv --venv-name <virtualenv name> '
              '--project-path <existing project path> ...\n  '
              'pyxa create venv --project-path <existing project path> ...')
venv_help = ('Create virtual environment in the existing project directory. '
             'This virtual environment is created at default '
             'path, "~/.<project directory>/<virtualenv name>/". The '
             'default name for the environment is "venv" but can be '
             'changed by specifying the "--venv-name" argument.')
venv_description = ('Description:\n  Creates virtual environment:\n\n  '
                    '- Virtual environment will be created in the project '
                    'directory.\n  '
                    '- Default name of the virtual environment is '
                    '"venv". You can override this by specifying '
                    '"--venv-name" argument.\n\n  '
                    'Virtual environment has access to global site packages '
                    'by default. Currently there isn\'t any option available '
                    'to override it.')
