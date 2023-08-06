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
"""Global functions."""

import logging
import os
from typing import Optional

from pyxa.utils.settings import DEFAULT_LOG_LEVEL, ENV_LOG_LEVEL_NAME

logger = logging.getLogger(__name__)


def set_log_level(log_level: Optional[int] = None):
    """Set logging level of pyXA to the provided log level."""
    if not log_level:
        log_level = os.environ.get(ENV_LOG_LEVEL_NAME, DEFAULT_LOG_LEVEL)
        log_level = logging.getLevelName(log_level)

    logging.getLogger('pyxa').setLevel(log_level)
