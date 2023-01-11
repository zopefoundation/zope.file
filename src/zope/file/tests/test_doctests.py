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
"""Unit tests for zope.file.

"""


__docformat__ = "reStructuredText"
import doctest
import unittest

from zope.component.testlayer import ZCMLFileLayer

import zope.file


ZopeFileLayer = ZCMLFileLayer(zope.file, 'configure.zcml')


def fromDocFile(path, **kwargs):
    try:
        from zope.file import testing
    except ImportError:
        def setUp(test):
            raise unittest.SkipTest("Unable to import zope.file.testing")
        suite = doctest.DocFileSuite(path, setUp=setUp, **kwargs)
    else:
        suite = testing.FunctionalBlobDocFileSuite(path, **kwargs)
    return suite


def fromSimpleDocFile(path, **kwargs):
    suite = doctest.DocFileSuite(path)
    suite.layer = ZopeFileLayer
    return suite


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("../README.rst"),
        doctest.DocFileSuite("../browser.rst"),
        fromSimpleDocFile("../adapters.rst"),
        fromDocFile('../contenttype.rst'),
        fromDocFile("../download.rst"),
        fromDocFile("../upload.rst"),
    ))
