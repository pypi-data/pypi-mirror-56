# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

logger = logging.getLogger("moon.engine.api.authz.managers")


class Managers(object):
    """Object that links managers together"""
    AuthzManager = None
