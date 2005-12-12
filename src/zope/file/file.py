"""Implementation of the file content type.

"""
__docformat__ = "reStructuredText"

import cStringIO

import persistent

import zope.app.location.interfaces
import zope.file.interfaces
import zope.interface


class File(persistent.Persistent):

    zope.interface.implements(
        zope.file.interfaces.IFile,
        zope.app.location.interfaces.ILocation)

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

    def open(self, mode="r"):
        if mode in ("r", "rb"):
            return Reader(self, mode)
        if mode in ("w", "wb"):
            return Writer(self, mode)
        raise ValueError("unsupported `mode` value")


class Accessor(object):
    """Base class for the reader and writer."""

    _closed = False
    _sio = None

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

    def close(self):
        if not self._closed:
            self._close()
            self._closed = True
            if "_sio" in self.__dict__:
                del self._sio

    def __getstate__(self):
        """Make sure the accessors can't be stored in ZODB."""
        cls = self.__class__
        raise TypeError("%s.%s instance is not picklable"
                        % (cls.__module__, cls.__name__))

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
        if self._sio is None:
            return 0L
        else:
            return self._sio.tell()

    def _get_stream(self):
        # get the right string io
        if self._sio is None:
            # create if we don't have one yet
            self._data = self.__parent__._data
            self._sio = cStringIO.StringIO(self._data)
        elif self._data is not self.__parent__._data:
            # if the data for the underlying object has changed,
            # update our view of the data:
            pos = self._sio.tell()
            self._data = self.__parent__._data
            if pos > len(self._data):
                # need to check if this is really right
                pos = len(self._data)
            self._sio = cStringIO.StringIO(self._data)
            self._sio.seek(pos)
        return self._sio


class Writer(Accessor):

    zope.interface.implements(
        zope.file.interfaces.IFileWriter)

    def flush(self):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        if self._sio is not None:
            self.__parent__._data = self._sio.getvalue()
            self.__parent__.size = len(self.__parent__._data)

    def write(self, data):
        if self._closed:
            raise ValueError("I/O operation on closed file")
        self._get_stream().write(data)

    def _get_stream(self):
        if self._sio is None:
            self._sio = cStringIO.StringIO()
        return self._sio

    def _close(self):
        self.flush()
