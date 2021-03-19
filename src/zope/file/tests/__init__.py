import unittest


def skipWithoutZopeFormlib(test):
    try:
        from zope import formlib
    except ImportError:
        formlib = None
    return unittest.skipIf(formlib is None, "Need zope.formlib")(test)
