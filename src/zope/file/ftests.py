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

import unittest

import zope.app.testing.functional


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        zope.app.testing.functional.FunctionalDocFileSuite("contenttype.txt"))
    suite.addTest(
        zope.app.testing.functional.FunctionalDocFileSuite("download.txt"))
    suite.addTest(
        zope.app.testing.functional.FunctionalDocFileSuite("upload.txt"))
    return suite
