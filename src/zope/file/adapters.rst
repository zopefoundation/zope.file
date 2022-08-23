==========
 Adapters
==========

The `zope.file` package provides some adapters to adapt file-like
objects to `zope.filerepresentation` conform objects. There is a
read-file adapter and a write-file adapter available. We start with a
regular `File` object:

   >>> from zope.file.file import File
   >>> f = File(parameters=dict(charset='utf-8'))
   >>> with f.open('w') as _: _ = _.write(b"hello")

Now we can turn this file into a read-only file which we can read and
whose size we can get:

   >>> from zope.filerepresentation.interfaces import IReadFile, IWriteFile
   >>> r = IReadFile(f)
   >>> r.read()
   'hello'

   >>> r.size()
   5

Writing to this read-only file is impossible, as the interface does
not require it:

   >>> r.write(b"some more content")  # doctest: +ELLIPSIS
   Traceback (most recent call last):
   AttributeError: 'ReadFileAdapter' object has no attribute 'write'...

With a write-file the opposite happens. We can write but not read:

   >>> w = IWriteFile(f)
   >>> w.write(b"some more content")
   >>> w.read()
   Traceback (most recent call last):
   AttributeError: 'WriteFileAdapter' object has no attribute 'read'

The delivered adapters really comply with the promised interfaces:

   >>> from zope.interface.verify import verifyClass, verifyObject
   >>> from zope.file.adapters import ReadFileAdapter, WriteFileAdapter
   >>> verifyClass(IReadFile, ReadFileAdapter)
   True

   >>> verifyObject(IReadFile, r)
   True

   >>> verifyClass(IWriteFile, WriteFileAdapter)
   True

   >>> verifyObject(IWriteFile, w)
   True
