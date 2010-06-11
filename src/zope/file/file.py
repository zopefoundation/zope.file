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
__docformat__ = "reStructuredText"

import persistent

import zope.location.interfaces
import zope.file.interfaces
import zope.interface

from ZODB.blob import Blob

class File(persistent.Persistent):

    zope.interface.implements(
        zope.file.interfaces.IFile,
        zope.location.interfaces.ILocation)

    __name__ = None
    __parent__ = None
    mimeType = None

    _data = ""
    size = 0

    def __init__(self, mimeType=None, parameters=None):
        self.mimeType = mimeType
        if parameters is None:
            parameters = {}
        else:
            parameters = dict(parameters)
        self.parameters = parameters
        self._data = Blob()
        fp = self._data.open('w')
        fp.write('')
        fp.close()

    def open(self, mode="r"):
        return self._data.open(mode)

    def openDetached(self):
        return file(self._data.committed(), 'rb')

    @property
    def size(self):
        if self._data == "":
            return 0
        reader = self.open()
        reader.seek(0,2)
        size = int(reader.tell())
        reader.close()
        return size
