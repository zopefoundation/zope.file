from zope import interface, component
import zope.app.filerepresentation.interfaces
from zope.file import interfaces

class ReadFileAdapter(object):
    component.adapts(interfaces.IFile)
    interface.implements(zope.app.filerepresentation.interfaces.IReadFile)
    
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
    interface.implements(zope.app.filerepresentation.interfaces.IWriteFile)
    
    def __init__(self, context):
        self.context = context

    def write(self, data):
        f = self.context.open('w')
        f.write(data)
        f.close()
