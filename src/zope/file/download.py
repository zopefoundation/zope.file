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

import cStringIO

import zope.interface
import zope.mimetype.interfaces
import zope.publisher.browser
import zope.publisher.http


class Download(zope.publisher.browser.BrowserView):

    def __call__(self):
        return DownloadResult(self.context, contentDisposition="attachment")


class Inline(zope.publisher.browser.BrowserView):

    def __call__(self):
        return DownloadResult(self.context, contentDisposition="inline")


class Display(zope.publisher.browser.BrowserView):

    def __call__(self):
        return DownloadResult(self.context)


class DownloadResult(object):
    """Result object for a download request."""

    zope.interface.implements(
        zope.publisher.http.IResult)

    def __init__(self, context, contentType=None, downloadName=None,
                 contentDisposition=None):
        if not contentType:
            cti = zope.mimetype.interfaces.IContentInfo(context, None)
            if cti is not None:
                contentType = cti.contentType
        contentType = contentType or "application/octet-stream"
        self.headers = ("Content-Type", contentType),

        downloadName = downloadName or context.__name__
        if contentDisposition:
            if downloadName:
                contentDisposition += (
                    '; filename="%s"' % downloadName.encode("utf-8")
                    )
            self.headers += ("Content-Disposition", contentDisposition),

        # This ensures that what's left has no connection to the
        # application/database; ZODB BLOBs will provide a equivalent
        # feature once available.
        #
        data = context.open("rb").read()
        self.headers += ("Content-Length", str(context.size)),
        self.body = bodyIterator(cStringIO.StringIO(data))


CHUNK_SIZE = 64 * 1024


def bodyIterator(f):
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            f.close()
            raise StopIteration()
        yield chunk
    f.close()
