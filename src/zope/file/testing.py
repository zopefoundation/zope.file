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
import re

from six.moves import urllib_parse as urllib

from zope.app.wsgi.testlayer import http
from zope.browser.interfaces import IAdding
from zope.browsermenu.menu import getFirstMenuItem
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from zope.container.interfaces import IContainerNamesContainer
from zope.container.interfaces import INameChooser

from zope.interface import implementer

from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserPublisher

from zope.security.proxy import removeSecurityProxy

from zope.traversing.browser.absoluteurl import absoluteURL

import zope.app.wsgi.testlayer
import zope.file
import zope.security.checker
import zope.testbrowser.wsgi
import zope.testing.renormalizing


class BrowserLayer(zope.testbrowser.wsgi.TestBrowserLayer,
                   zope.app.wsgi.testlayer.BrowserLayer):
    pass


ZopeFileLayer = BrowserLayer(zope.file)


def FunctionalBlobDocFileSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['getRootFolder'] = ZopeFileLayer.getRootFolder
    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp', lambda x: None)
    def setUp(test):
        wsgi_app = ZopeFileLayer.make_wsgi_app()
        def _http(query_str, *args, **kwargs):
            # Strip leading \n
            query_str = query_str.lstrip()
            return http(wsgi_app, query_str, *args, **kwargs)

        test.globs['http'] = _http
        kwsetUp(test)
    kw['setUp'] = setUp

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.REPORT_NDIFF
                             | doctest.NORMALIZE_WHITESPACE)

    kw['checker'] = zope.testing.renormalizing.RENormalizing([
        # Py3k renders bytes where Python2 used native strings...
        (re.compile(r"^b'"), "'"),
        (re.compile(r'^b"'), '"'),
    ])

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = ZopeFileLayer
    return suite


@implementer(IAdding)
class Adding(BrowserView):
    # set in BrowserView.__init__
    request = None
    context = None
    contentName = None # usually set by Adding traverser

    def add(self, content):
        container = self.context
        name = self.contentName
        chooser = INameChooser(container)

        request = self.request
        name = request.get('add_input_name', name)
        assert name

        chooser.checkName(name, content)

        container[name] = content
        self.contentName = name # Set the added object Name
        return container[name]

    def nextURL(self):
        return absoluteURL(self.context, self.request) + '/@@contents.html'

    def nameAllowed(self):
        """Return whether names can be input by the user."""
        return not IContainerNamesContainer.providedBy(self.context)


class Contents(BrowserView):

    error = ''
    message = ''
    normalButtons = False
    specialButtons = False
    supportsRename = False
    contents = ViewPageTemplateFile('tests/contents.pt')
    contentsMacros = contents

    def listContentInfo(self):
        return self._normalListContentsInfo()

    def _normalListContentsInfo(self):
        # Remove the security proxy to work around an issue with
        # iterating proxied BTree objects on PyPy (pure-python implementation
        # of BTrees.) See https://github.com/zopefoundation/zope.security/issues/20
        items = removeSecurityProxy(self.context.items())
        info = [self._extractContentInfo(x) for x in items]
        return info

    def _extractContentInfo(self, item):
        info = {}
        oid, obj = item
        info['id'] = info['cb_id'] = oid
        info['object'] = obj
        info['url'] = urllib.quote(oid.encode('utf-8'))
        return info

@implementer(IBrowserPublisher)
class ManagementViewSelector(BrowserView):
    """View that selects the first available management view.

    Support 'zmi_views' actions like: 'javascript:alert("hello")',
    '../view_on_parent.html' or '++rollover++'.
    """
    # Copied from zope.app.publication

    def browserDefault(self, request):
        return self, ()

    def __call__(self):
        item = getFirstMenuItem('zmi_views', self.context, self.request)

        if item:
            redirect_url = item['action']
            if not (redirect_url.startswith('../') or \
                    redirect_url.lower().startswith('javascript:') or \
                    redirect_url.lower().startswith('++')):
                self.request.response.redirect(redirect_url)
                return u''

        # The zope.app.publication version would redirect to /
        # with self.request.response.redirect('.) and return u''.
        # But our tests never get here.
        raise AssertionError("We shouldn't get here") # pragma: no cover
