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
"""Event support code.

"""
__docformat__ = "reStructuredText"


def updateMimeType(file, event):
    """Update the file's mimeType on a change.

    If the current mimeType value is known to be legal for the new
    content type, leave it alone.  If not, set the mimeType attribute
    to the first value from the list of known MIME types for the
    content type.

    """
    if event.newContentType is not None:
        types = event.newContentType.getTaggedValue("mimeTypes")
        if file.mimeType not in types:
            file.mimeType = types[0]
