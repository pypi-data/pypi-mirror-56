#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains manager that handles Plot Twist DCC Menu
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import webbrowser

from Qt.QtWidgets import *

from tpPyUtils import decorators

import artellapipe.register
from artellapipe.utils import resource
import artellapipe.libs.kitsu as kitsu_lib


class PlotTwistMenu(artellapipe.Menu, object):
    def __init__(self):

        self._kitsu_action_object_name = None

        super(PlotTwistMenu, self).__init__()

    def set_project(self, project):
        self._kitsu_action_object_name = '{}_kitsu'.format(self._menu_name)
        super(PlotTwistMenu, self).set_project(project)

    def create_menus(self):
        valid_creation = super(PlotTwistMenu, self).create_menus()
        if not valid_creation:
            return False

        self.create_kitsu_menu()

    def get_menu_names(self):
        menu_names = super(PlotTwistMenu, self).get_menu_names()
        if self._kitsu_action_object_name not in menu_names:
            menu_names.append(self._kitsu_action_object_name)

        return menu_names

    def create_kitsu_menu(self):
        self._kitsu_action = QAction(self._parent.menuBar())
        self._kitsu_action.setIcon(resource.ResourceManager().icon('kitsu'))
        self._parent.menuBar().addAction(self._kitsu_action)
        self._kitsu_action.setObjectName(self._kitsu_action_object_name)
        self._kitsu_action.triggered.connect(self._on_kitsu_open)

    def _on_kitsu_open(self):
        """
        Internal callback function that is called when kitsu action is pressed
        """

        project_url = kitsu_lib.config.get('project_url', None)
        if not project_url:
            return None

        webbrowser.open(project_url)


@decorators.Singleton
class PlotTwistMenuManagerSingleton(PlotTwistMenu, object):
    def __init__(self):
        PlotTwistMenu.__init__(self)


artellapipe.register.register_class('MenuMgr', PlotTwistMenuManagerSingleton)
