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

from zope.file import testing

def fromDocFile(path):
    suite = testing.FunctionalBlobDocFileSuite(path)
    suite.layer = testing.ZopeFileLayer
    return suite

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("README.txt"),
        doctest.DocFileSuite("browser.txt"),
        fromDocFile("contenttype.txt"),
        fromDocFile("download.txt"),
        fromDocFile("upload.txt"),
        ))
