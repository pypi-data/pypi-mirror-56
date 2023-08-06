#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementations for rig asset files
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import logging

import tpDccLib as tp

import artellapipe
from artellapipe.core import file

LOGGER = logging.getLogger()


class PlotTwistLightRigFile(file.ArtellaFile, object):
    def __init__(self, file_name, file_path=None, file_extension=None):
        super(PlotTwistLightRigFile, self).__init__(
            file_name=file_name, file_path=file_path, file_extension=file_extension)

    def get_template_dict(self):
        """
        Implements get_template_dict() function
        :return: dict
        """

        return {
            'assets_path': artellapipe.AssetsMgr().get_assets_path(),
            'light_rig_name': self.name
        }

    def _reference_file(self, file_path, *args, **kwargs):
        LOGGER.info('Referencing: {}'.format(file_path))
        tp.Dcc.reference_file(file_path)
