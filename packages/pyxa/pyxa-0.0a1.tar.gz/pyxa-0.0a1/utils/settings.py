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
"""Global pyXA settings."""

# Settings for the package.
PACKAGE_NAME = 'pyxa'
PROJECT_NAME = 'pyXA'
AI_NAME = 'Charlotte'
# This package adheres to Semantic Versioning Specification (SemVer)
# starting with version 0.0a1.
PACKAGE_VERSION = '0.0a1'

# Author details.
AUTHOR = 'XA'
AUTHOR_EMAIL = MAINTAINER_EMAIL = 'xames3.charlotte@gmail.com'

# Local time zone details.
# You can find all the choices here:
# https://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Kolkata'

# Language used by the project
# You can find all the choices here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

# Default encoding used for all read-write objects.
DEFAULT_CHARSET = 'utf-8'

# Default package structure.
# You can override this while creating project. pyXA recommends you not
# to do it so.
# User config settings.
USER_PATH = 'user'
USER_PROFILE_PATH = USER_PATH + '/profile.yml'
# Cache & garbage collector settings.
FILES_PATH = 'files'
TEMP_PATH = FILES_PATH + '/temp/'
CACHE_PATH = TEMP_PATH + '/cache/'
# Database settings.
DATABASE_PATH = 'database'
DATABASE_FILE_PATH = DATABASE_PATH + '/tracker_store.db'
# Virtual environment settings.
VIRTUALENV_NAME = 'venv'
VIRTUALENV_PATH = VIRTUALENV_NAME + '/'
VIRTUALENV_ACTIVATE_PATH = VIRTUALENV_NAME + '/Scripts/activate'
VIRTUALENV_DEFAULT_SETTING = '--system-site-packages'
# Frontend & UI settings.
FRONTEND_PATH = 'frontend'

# Ports details.
# This port details can be override manually later.
LOCALHOST = 'localhost'
ACTION_SERVER_PORT = 6969
NAUGHTY_HOST_PORT = 1414
TEST_HOST_PORT = 2121

# Logging levels.
# Sets the logging level to INFO.
ENV_LOG_LEVEL_NAME = 'PYXA_LOG_LEVEL'
DEFAULT_LOG_LEVEL = 'INFO'

# Secret keys.
# Secret keys are the API keys that are needed for using some of the
# features of pyXA. You can find those details in the respective module.
GOOGLE_CLOUD_KEY = ''
DARKSKY_KEY = ''
TWILIO_KEY = ''
