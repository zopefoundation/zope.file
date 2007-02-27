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

import sys
import cStringIO

import persistent

import zope.location.interfaces
import zope.file.interfaces
import zope.interface

from ZODB.Blobs.Blob import Blob

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
        if mode.startswith("r"):
            return Reader(self, mode)
        if mode.startswith("w"):
            return Writer(self, mode)
        raise ValueError("unsupported `mode` value")

    def openDetached(self):
        return self._data.openDetached()

    @property
    def size(self):
        if self._data == "":
            return 0
        reader = self.open()
        reader.seek(0,2)
        size = int(reader.tell())
        reader.close()
        return size


class Accessor(object):
    """Base class for the reader and writer."""

    _closed = False
    _sio = None
    _write = False
    mode = None

    # XXX Accessor objects need to have an __parent__ to support the
    # security machinery, but they aren't ILocation instances since
    # they aren't addressable via URL.
    #
    # There needs to be an interface for this in Zope 3, but that's a
    # large task since it affects lots of Z3 code.  __parent__ should
    # be defined by an interface from which ILocation is derived.

    def __init__(self, file, mode):
        self.__parent__ = file
        self.mode = mode
        self._stream = self.__parent__._data.open(mode)

    def close(self):
        if not self._closed:
            self._close()
            self._closed = True

    def __getstate__(self):
        """Make sure the accessors can't be stored in ZODB."""
        cls = self.__class__
        raise TypeError("%s.%s instance is not picklable"
                        % (cls.__module__, cls.__name__))

    def _get_stream(self):
        return self._stream

    def _close(self):
        pass


class Reader(Accessor):

    zope.interface.implements(
        zope.file.interfaces.IFileReader)

    _data = File._data

    def read(self, size=-1):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        return self._get_stream().read(size)

    def seek(self, offset, whence=0):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        if whence not in (0, 1, 2):
            raise ValueError("illegal value for `whence`")
        self._get_stream().seek(offset, whence)

    def tell(self):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        return int(self._get_stream().tell())

    def _close(self):
        self._get_stream().close()


class Writer(Accessor):

    zope.interface.implements(
        zope.file.interfaces.IFileWriter)

    _write = True

    def flush(self):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        self._get_stream().flush()
    
    def write(self, data):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        self._get_stream().write(data)

    def _close(self):
        self._get_stream().close()

