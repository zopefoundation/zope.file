=====================
Presentation Adapters
=====================

Object size
-----------

The size of the file as presented in the contents view of a container is
provided using an adapter implementing the `zope.size.interfaces.ISized`
interface. Such an adapter is available for the file object.

Let's do some imports and create a new file object:

  >>> from zope.file.file import File
  >>> from zope.file.browser import Sized
  >>> from zope.size.interfaces import ISized

  >>> f = File()
  >>> f.size
  0

  >>> s = Sized(f)
  >>> ISized.providedBy(s)
  True
  >>> s.sizeForSorting()
  ('byte', 0)
  >>> s.sizeForDisplay()
  u'0 KB'

Let's add some content to the file:

  >>> with f.open('w') as w:
  ...    _ =  w.write(b"some text")

The sized adapter now reflects the updated size:

  >>> s.sizeForSorting()
  ('byte', 9)
  >>> s.sizeForDisplay()
  u'1 KB'

Let's try again with a larger file size:

  >>> with f.open('w') as w:
  ...    _ = w.write(b"x" * (1024*1024+10))

  >>> s.sizeForSorting()
  ('byte', 1048586)
  >>> m = s.sizeForDisplay()
  >>> m
  u'${size} MB'
  >>> m.mapping
  {'size': '1.00'}

And still a bigger size:

  >>> with f.open('w') as w:
  ...    _ = w.write(b"x" * 3*512*1024)

  >>> s.sizeForSorting()
  ('byte', 1572864)
  >>> m = s.sizeForDisplay()
  >>> m
  u'${size} MB'
  >>> m.mapping
  {'size': '1.50'}
