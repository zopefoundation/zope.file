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
"""Interfaces for zope.file.

These interfaces support efficient access to file data.

"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.mimetype.interfaces
import zope.schema

from zope.file.i18n import _


class IFile(zope.mimetype.interfaces.IContentTypeAware):
    """File content object for Zope."""

    def open(mode="r"):
        """Return an object providing access to the file data.

        Allowed values for `mode` are 'r' (read); 'w' (write); 'a' (append) and
        'r+' (read/write).  Other values cause `ValueError` to be raised.

        If the file is opened in read mode, an object with an API (but
        not necessarily interface) of `IFileReader` is returned; if
        opened in write mode, an object with an API of `IFileWriter` is
        returned; if in read/write, an object that implements both is
        returned.

        All readers and writers operate in 'binary' mode.

        """

    def openDetached():
        """Return file data disconnected from database connection.

        Read access only.
        """

    size = zope.schema.Int(
        title=_("Size"),
        description=_("Size in bytes"),
        readonly=True,
        required=True,
        )


# The remaining interfaces below serve only to document the kind of APIs
# to be expected, as described in IFile.open above.

class IFileAccessor(zope.interface.Interface):
    """Base accessor for `IFileReader` and `IFileWriter`."""

    def close():
        """Release the accessor.

        Resources held by the accessor are freed, and further use of
        the accessor will result in a `ValueError` exception.

        """

    mode = zope.schema.BytesLine(
        title=_("Open mode passed to the corresponding file's open() method,"
                " or the default value if not passed."),
        required=True,
        )


class IFileReader(IFileAccessor):
    """Read-accessor for file objects.

    The methods here mirror the corresponding portions of the API for
    Python file objects.

    """

    def read(size=-1):
        """Read at most `size` bytes from the reader.

        If the size argument is negative or omitted, read all data
        until EOF is reached.  The bytes are returned as a str.  An
        empty string is returned when EOF is encountered immediately.

        """

    def seek(offset, whence=0):
        """Set the reader's current position.

        The `offset` is a number of bytes.  The direction and source
        of the measurement is determined by the `whence` argument.

        The `whence` argument is optional and defaults to 0 (absolute
        file positioning); other recognized values are 1 (seek
        relative to the current position) and 2 (seek relative to the
        end).

        There is no return value.

        """

    def tell():
        """Return the current position, measured in bytes."""


class IFileWriter(IFileAccessor):
    """Write-accessor for file objects.

    The methods here mirror the corresponding portions of the API for
    Python file objects.

    """

    def flush():
        """Ensure the file object has been updated.

        This is used to make sure that any data buffered in the
        accessor is stored in the file object, allowing other
        accessors to use it.

        """

    def write(bytes):
        """Write a string to the file.

        Due to buffering, the string may not actually show up in the
        file until the `flush()` or `close()` method is called.

        There is no return value.

        """
