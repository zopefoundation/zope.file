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

@component.adapter(interfaces.IFile)
@interface.implementer(zope.filerepresentation.interfaces.IReadFile)
class ReadFileAdapter(object):

    def __init__(self, context):
        self.context = context

    def size(self):
        return self.context.size

    def read(self):
        with self.context.open() as f:
            return f.read()

@component.adapter(interfaces.IFile)
@interface.implementer(zope.filerepresentation.interfaces.IWriteFile)
class WriteFileAdapter(object):

    def __init__(self, context):
        self.context = context

    def write(self, data):
        with self.context.open('w') as f:
            f.write(data)
