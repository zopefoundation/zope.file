===========
File Object
===========

The `zope.file` package provides a content object used to store a
file.  The interface supports efficient upload and download.  Let's
create an instance:

  >>> from zope.file.file import File
  >>> f = File()

The object provides a limited number of data attributes.  The
`mimeType` attribute is used to store the preferred MIME
content-type value for the data:

  >>> f.mimeType

  >>> f.mimeType = "text/plain"
  >>> f.mimeType
  'text/plain'

  >>> f.mimeType = "application/postscript"
  >>> f.mimeType
  'application/postscript'

The `parameters` attribute is a mapping used to store the content-type
parameters.  This is where encoding information can be found when
applicable (and available):

  >>> f.parameters
  {}
  >>> f.parameters["charset"] = "us-ascii"
  >>> f.parameters["charset"]
  'us-ascii'

File objects also sport a `size` attribute that provides the number of
bytes in the file:

  >>> f.size
  0

The object supports efficient upload and download by providing all
access to content data through accessor objects that provide (subsets
of) Python's file API.

A file that hasn't been written to is empty.  We can get a reader by calling
`open()`. Note that all blobs are binary, thus the mode always contains a
'b':

  >>> r = f.open("r")
  >>> r.mode
  'rb'

The `read()` method can be called with a non-negative integer argument
to specify how many bytes to read, or with a negative or omitted
argument to read to the end of the file:

  >>> r.read(10)
  ''
  >>> r.read()
  ''
  >>> r.read(-1)
  ''

Once the accessor has been closed, we can no longer read from it:

  >>> r.close()
  >>> r.read()
  Traceback (most recent call last):
  ValueError: I/O operation on closed file

We'll see that readers are more interesting once there's data in the
file object.

Data is added by using a writer, which is also created using the
`open()` method on the file, but requesting a write file mode:

  >>> w = f.open("w")
  >>> w.mode
  'wb'

The `write()` method is used to add data to the file, but note that
the data may be buffered in the writer:

  >>> w.write("some text ")
  >>> w.write("more text")

The `flush()` method ensure that the data written so far is written to
the file object:

  >>> w.flush()

We need to close the file first before determining its file size

  >>> w.close()
  >>> f.size
  19

We can now use a reader to see that the data has been written to the
file:

  >>> w = f.open("w")
  >>> w.write('some text more text')
  >>> w.write(" still more")
  >>> w.close()
  >>> f.size
  30


Now create a new reader and let's perform some seek operations.

  >>> r = f.open()

The reader also has a `seek()` method that can be used to back up or
skip forward in the data stream.  Simply passing an offset argument,
we see that the current position is moved to that offset from the
start of the file:

  >>> r.seek(20)
  >>> r.read()
  'still more'

That's equivalent to passing 0 as the `whence` argument:

  >>> r.seek(20, 0)
  >>> r.read()
  'still more'

We can skip backward and forward relative to the current position by
passing 1 for `whence`:

  >>> r.seek(-10, 1)
  >>> r.read(5)
  'still'
  >>> r.seek(2, 1)
  >>> r.read()
  'ore'

We can skip to some position backward from the end of the file using
the value 2 for `whence`:

  >>> r.seek(-10, 2)
  >>> r.read()
  'still more'

  >>> r.seek(0)
  >>> r.seek(-4, 2)
  >>> r.read()
  'more'

  >>> r.close()


Attempting to write to a closed writer raises an exception:


  >>> w = f.open('w')
  >>> w.close()

  >>> w.write('foobar')
  Traceback (most recent call last):
  ValueError: I/O operation on closed file

Similarly, using `seek()` or `tell()` on a closed reader raises an
exception:

  >>> r.close()
  >>> r.seek(0)
  Traceback (most recent call last):
  ValueError: I/O operation on closed file

  >>> r.tell()
  Traceback (most recent call last):
  ValueError: I/O operation on closed file

