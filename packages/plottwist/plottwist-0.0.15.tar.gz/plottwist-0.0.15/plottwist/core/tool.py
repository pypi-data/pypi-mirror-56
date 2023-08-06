#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains core classes for tools
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import logging

import artellapipe.register
from artellapipe.core import tool

LOGGER = logging.getLogger()


class PlotTwistTool(tool.Tool, object):
    def __init__(self, project, config, parent=None):
        super(PlotTwistTool, self).__init__(project=project, config=config, parent=parent)

    def set_attacher(self, attacher):
        super(PlotTwistTool, self).set_attacher(attacher=attacher)

        if self._attacher and hasattr(self._attacher, 'try_kitsu_login'):
            LOGGER.info('Trying to login into Kitsu ...')
            self._attacher.try_kitsu_login()


artellapipe.register.register_class('Tool', PlotTwistTool)
