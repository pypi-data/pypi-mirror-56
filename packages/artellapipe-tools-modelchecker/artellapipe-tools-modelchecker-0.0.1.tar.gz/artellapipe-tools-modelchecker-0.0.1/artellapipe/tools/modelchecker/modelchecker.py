#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains publisher implementation for Artella
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import artellapipe


class ArtellaModelChecker(artellapipe.PyblishTool, object):

    def __init__(self, project, config):

        super(ArtellaModelChecker, self).__init__(project=project, config=config)


# def run(project):
#
#     if tp.is_maya():
#         pyblish.api.register_host('maya')
#     elif tp.is_houdini():
#         pyblish.api.register_host('houdini')
#
#     win = ArtellaPublisher(project=project)
#     win.show()

#
#     pyblish_win = pyblish_lite.show()
#     win.set_pyblish_window(pyblish_win)
#
#     return win
