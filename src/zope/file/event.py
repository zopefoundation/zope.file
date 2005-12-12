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
