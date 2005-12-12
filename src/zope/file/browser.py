"""Presentation adapters for zope.file.

"""
__docformat__ = "reStructuredText"

import zope.app.size
import zope.app.size.interfaces
import zope.component
import zope.file.interfaces
import zope.interface


class Sized(object):

    zope.interface.implements(
        zope.app.size.interfaces.ISized)

    zope.component.adapts(
        zope.file.interfaces.IFile)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        return "byte", self.context.size

    def sizeForDisplay(self):
        return zope.app.size.byteDisplay(self.context.size)
