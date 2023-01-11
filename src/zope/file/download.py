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
            # Headers must be native strings,
            # but characters greater than 256 will fail to be encoded
            # by the WSGI server, which should be using latin-1. The
            # solution is to smuggle them through using double encoding,
            # allowing the final recipient to decode its string using utf-8
            downloadName = downloadName.encode('utf-8').decode('latin-1')

            contentDisposition += (
                '; filename="%s"' % downloadName
            )
        headers += ("Content-Disposition", contentDisposition),

    if contentLength is None:
        contentLength = context.size
    headers += ("Content-Length", str(contentLength)),
    return headers


@zope.interface.implementer(zope.publisher.interfaces.http.IResult)
class DownloadResult:
    """Result object for a download request."""

    def __init__(self, context):
        self._iter = bodyIterator(
            zope.security.proxy.removeSecurityProxy(context.openDetached()))

    def __iter__(self):
        return self._iter


CHUNK_SIZE = 64 * 1024


def bodyIterator(f):
    try:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                return
            yield chunk
    finally:
        f.close()
