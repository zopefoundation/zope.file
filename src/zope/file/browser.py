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
"""Presentation adapters for zope.file.

"""
__docformat__ = "reStructuredText"

import zope.size
import zope.size.interfaces
import zope.component
import zope.file.interfaces
import zope.interface


class Sized(object):

    zope.interface.implements(
        zope.size.interfaces.ISized)

    zope.component.adapts(
        zope.file.interfaces.IFile)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        return "byte", self.context.size

    def sizeForDisplay(self):
        return zope.size.byteDisplay(self.context.size)
