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
import re
import unittest

from zope.component.testlayer import ZCMLFileLayer
from zope.testing import renormalizing

import zope.file


checker = renormalizing.RENormalizing([
    # Python 3 unicode removed the "u".
    (re.compile("u('.*?')"), r"\1"),
    (re.compile('u(".*?")'), r"\1"),
    # Python 3 bytes added the "b".
    (re.compile("b('.*?')"), r"\1"),
    (re.compile('b(".*?")'), r"\1"),
])


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
    suite = doctest.DocFileSuite(path, checker=checker)
    suite.layer = ZopeFileLayer
    return suite


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("../README.rst", checker=checker),
        doctest.DocFileSuite("../browser.rst", checker=checker),
        fromSimpleDocFile("../adapters.rst", checker=checker),
        fromDocFile('../contenttype.rst', checker=checker),
        fromDocFile("../download.rst", checker=checker),
        fromDocFile("../upload.rst", checker=checker),
    ))
