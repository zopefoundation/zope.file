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
"""Download view for files.

"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.mimetype.interfaces
import zope.publisher.browser
import zope.publisher.interfaces.http
import zope.security.proxy

class Download(zope.publisher.browser.BrowserView):

    def __call__(self):
        for k, v in getHeaders(self.context, contentDisposition="attachment"):
            self.request.response.setHeader(k, v)
        return DownloadResult(self.context)


class Inline(zope.publisher.browser.BrowserView):

    def __call__(self):
        for k, v in getHeaders(self.context, contentDisposition="inline"):
            self.request.response.setHeader(k, v)
        return DownloadResult(self.context)


class Display(zope.publisher.browser.BrowserView):

    def __call__(self):
        for k, v in getHeaders(self.context):
            self.request.response.setHeader(k, v)
        return DownloadResult(self.context)

def getHeaders(context, contentType=None, downloadName=None,
               contentDisposition=None, contentLength=None):
        if not contentType:
            cti = zope.mimetype.interfaces.IContentInfo(context, None)
            if cti is not None:
                contentType = cti.contentType
        contentType = contentType or "application/octet-stream"
        headers = ("Content-Type", contentType),

        downloadName = downloadName or context.__name__
        if contentDisposition:
            if downloadName:
                contentDisposition += (
                    '; filename="%s"' % downloadName.encode("utf-8")
                    )
            headers += ("Content-Disposition", contentDisposition),

        if contentLength is None:
            contentLength = context.size
        headers += ("Content-Length", str(contentLength)),
        return headers

class DownloadResult(object):
    """Result object for a download request."""

    zope.interface.implements(zope.publisher.interfaces.http.IResult)

    def __init__(self, context):
        self._iter = bodyIterator(
            zope.security.proxy.removeSecurityProxy(context.openDetached()))

    def __iter__(self):
        return self._iter

CHUNK_SIZE = 64 * 1024


def bodyIterator(f):
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            f.close()
            raise StopIteration()
        yield chunk
    f.close()
