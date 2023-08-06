#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base wrapper classes to create DCC windows
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import artellapipe.register
from artellapipe.widgets import window
from artellapipe.libs.kitsu.widgets import userinfo


class PlotTwistWindowStatusBar(window.ArtellaWindowStatusBar, object):
    def __init__(self, parent=None):
        super(PlotTwistWindowStatusBar, self).__init__(parent=parent)

        self._user_info = userinfo.KitsuUserInfo(project=self._project, parent=parent)
        self.main_layout.insertWidget(self.main_layout.count() - 1, self._user_info)

    def set_project(self, project):
        super(PlotTwistWindowStatusBar, self).set_project(project)

        self._user_info.set_project(project)

    def try_kitsu_login(self):
        """
        Function that tries to login into Kitsu with stored credentials
        :return: bool
        """

        valid_login = self._user_info.try_kitsu_login()
        if valid_login:
            return True

        return False


class PlotTwistWindow(window.ArtellaWindow, object):

    STATUS_BAR_WIDGET = PlotTwistWindowStatusBar

    def __init__(self, *args, **kwargs):
        super(PlotTwistWindow, self).__init__(*args, **kwargs)

    def try_kitsu_login(self):
        """
        Function that tries to login into Kitsu with stored credentials
        :return: bool
        """

        return self._status_bar.try_kitsu_login()


artellapipe.register.register_class('Window', PlotTwistWindow)
