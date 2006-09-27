##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Functional tests for zope.file.

"""
__docformat__ = "reStructuredText"

import os.path
import unittest

import zope.app.testing.functional

here = os.path.dirname(os.path.realpath(__file__))

ZopeFileLayer = zope.app.testing.functional.ZCMLLayer(
    os.path.join(here, "ftesting.zcml"), __name__, "ZopeFileLayer")


def fromDocFile(path):
    suite = zope.app.testing.functional.FunctionalDocFileSuite(path)
    suite.layer = ZopeFileLayer
    return suite

def test_suite():
    return unittest.TestSuite([
        fromDocFile("contenttype.txt"),
        fromDocFile("download.txt"),
        fromDocFile("upload.txt"),
        ])
