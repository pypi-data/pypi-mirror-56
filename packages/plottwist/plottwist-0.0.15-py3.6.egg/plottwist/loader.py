#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella loader implementation for Plot Twist
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"


import os
import inspect
import logging.config


def init(do_reload=False, import_libs=True, dev=False, artella_configs_path=None):
    """
    Initializes Plot Twist library
    """

    # Load logger configuration
    logging.config.fileConfig(get_logging_config(), disable_existing_loggers=False)

    # Without default_integrations=False, PyInstaller fails during launcher generation
    if not dev:
        import sentry_sdk
        try:
            sentry_sdk.init("https://d71a4ba272374d7fb845269bb2aebf37@sentry.io/1816355")
        except (RuntimeError, ImportError):
            sentry_sdk.init("https://d71a4ba272374d7fb845269bb2aebf37@sentry.io/1816355", default_integrations=False)

    from tpPyUtils import importer

    class PlotTwistCore(importer.Importer, object):
        def __init__(self):
            super(PlotTwistCore, self).__init__(module_name='plottwist')

        def get_module_path(self):
            """
            Returns path where plot twist core module is stored
            :return: str
            """

            try:
                mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
            except Exception:
                try:
                    mod_dir = os.path.dirname(__file__)
                except Exception:
                    try:
                        import tpDccLib
                        mod_dir = tpDccLib.__path__[0]
                    except Exception:
                        return None

            return mod_dir

    packages_order = [
        'plottwist.core'
    ]

    if import_libs:
        import tpPyUtils
        tpPyUtils.init(do_reload=do_reload)
        import tpDccLib
        tpDccLib.init(do_reload=do_reload)
        import tpQtLib
        tpQtLib.init(do_reload=do_reload)
        import tpNameIt
        tpNameIt.init(do_reload=do_reload)
        import artellapipe.loader
        artellapipe.loader.init(do_reload=do_reload, dev=dev)

    from plottwist.core import project

    plottwist_core_importer = importer.init_importer(importer_class=PlotTwistCore, do_reload=False)
    plottwist_core_importer.import_packages(
        only_packages=False,
        order=packages_order,
        skip_modules=['plottwist.bootstrap']
    )
    if do_reload:
        plottwist_core_importer.reload_all()

    create_logger_directory()

    from artellapipe.utils import resource
    resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
    resource.ResourceManager().register_resource(resources_path, 'project')
    resource.ResourceManager().register_resource(os.path.join(resources_path, 'icons', 'shelf'), 'shelf')

    import artellapipe.loader
    artellapipe.loader.set_project(project.PlotTwist, do_reload=do_reload)


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """

    artellapipe_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'plottwist', 'logs'))
    if not os.path.isdir(artellapipe_logger_dir):
        os.makedirs(artellapipe_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    create_logger_directory()

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def get_logging_level():
    """
    Returns logging level to use
    :return: str
    """

    if os.environ.get('PLOTTWIST_LOG_LEVEL', None):
        return os.environ.get('PLOTTWIST_LOG_LEVEL')

    return os.environ.get('PLOTTWIST_LOG_LEVEL', 'WARNING')
