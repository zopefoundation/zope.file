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
"""Implementation of the file content type.

"""


from contextlib import closing

import persistent
import zope.interface
import zope.location.interfaces
from ZODB.blob import Blob

import zope.file.interfaces


@zope.interface.implementer(
    zope.file.interfaces.IFile,
    zope.location.interfaces.ILocation)
class File(persistent.Persistent):

    __name__ = None
    __parent__ = None
    mimeType = None

    _data = b""
    size = 0

    def __init__(self, mimeType=None, parameters=None):
        self.mimeType = mimeType
        if parameters is None:
            parameters = {}
        else:
            parameters = dict(parameters)
        self.parameters = parameters
        blob = self._data = Blob()
        with blob.open('w') as fp:
            fp.write(b'')

    # Note that if we are security proxied, we may not be able to use
    # __exit__ on the return values from open*, meaning they can't directly
    # be used in a with statement.

    def open(self, mode="r"):
        return self._data.open(mode)

    def openDetached(self):
        return open(self._data.committed(), 'rb')

    @property
    def size(self):
        if self._data == b"":  # pragma: no cover
            # It shouldn't be possible to get here; perhaps this is
            # compatibility code for old objects in existing databases?
            return 0

        with closing(self.open()) as reader:
            reader.seek(0, 2)
            size = int(reader.tell())

        return size
