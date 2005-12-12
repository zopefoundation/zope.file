"""Unit tests for zope.file.

"""
__docformat__ = "reStructuredText"

import unittest

from zope.testing import doctest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocFileSuite("README.txt"))
    suite.addTest(doctest.DocFileSuite("browser.txt"))
    return suite
