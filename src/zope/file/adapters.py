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
from zope import interface, component
import zope.filerepresentation.interfaces
from zope.file import interfaces

class ReadFileAdapter(object):
    component.adapts(interfaces.IFile)
    interface.implements(zope.filerepresentation.interfaces.IReadFile)

    def __init__(self, context):
        self.context = context

    def size(self):
        return self.context.size

    def read(self):
        f = self.context.open()
        val = f.read()
        f.close()
        return val

class WriteFileAdapter(object):
    component.adapts(interfaces.IFile)
    interface.implements(zope.filerepresentation.interfaces.IWriteFile)

    def __init__(self, context):
        self.context = context

    def write(self, data):
        f = self.context.open('w')
        f.write(data)
        f.close()
