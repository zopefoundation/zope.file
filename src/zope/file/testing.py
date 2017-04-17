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

import doctest
import os.path

from zope.app.wsgi.testlayer import http
import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi

import zope.file


class BrowserLayer(zope.testbrowser.wsgi.TestBrowserLayer,
                   zope.app.wsgi.testlayer.BrowserLayer):
    pass


ZopeFileLayer = BrowserLayer(zope.file)


def FunctionalBlobDocFileSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['getRootFolder'] = ZopeFileLayer.getRootFolder
    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        wsgi_app = ZopeFileLayer.make_wsgi_app()
        def _http(query_str, *args, **kwargs):
            # Strip leading \n
            query_str = query_str[1:]
            return http(wsgi_app, query_str, *args, **kwargs)

        test.globs['http'] = _http
        if kwsetUp is not None:
            kwsetUp(test)
    kw['setUp'] = setUp

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.REPORT_NDIFF
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = ZopeFileLayer
    return suite
