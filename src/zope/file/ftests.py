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
