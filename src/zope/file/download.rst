==========================
 Downloading File Objects
==========================

The file content type provides a view used to download the file,
regardless of the browser's default behavior for the content type.
This relies on browser support for the Content-Disposition header.

The download support is provided by two distinct objects:  A view that
provides the download support using the information in the content
object, and a result object that can be used to implement a file
download by other views.  The view can override the content-type or the
filename suggested to the browser using the standard IResponse.setHeader
method.

Note that result objects are intended to be used once and then
discarded.

Let's start by creating a file object we can use to demonstrate the
download support:

  >>> import transaction
  >>> from zope.file.file import File
  >>> f = File()
  >>> getRootFolder()['file'] = f
  >>> transaction.commit()

Headers
=======

Now, let's get the headers for this file.  We use a utility function called
``getHeaders``:

  >>> from zope.file.download import getHeaders
  >>> headers = getHeaders(f, contentDisposition='attachment')

Since there's no suggested download filename on the file, the
Content-Disposition header doesn't specify one, but does indicate that
the response body be treated as a file to save rather than to apply
the default handler for the content type:

  >>> sorted(headers)
  [('Content-Disposition', 'attachment; filename="file"'),
   ('Content-Length', '0'),
   ('Content-Type', 'application/octet-stream')]


Note that a default content type of 'application/octet-stream' is
used.

If the file object specifies a content type, that's used in the headers
by default:

  >>> f.mimeType = "text/plain"
  >>> headers = getHeaders(f, contentDisposition='attachment')
  >>> sorted(headers)
  [('Content-Disposition', 'attachment; filename="file"'),
   ('Content-Length', '0'),
   ('Content-Type', 'text/plain')]

Alternatively, a content type can be specified to ``getHeaders``:

  >>> headers = getHeaders(f, contentType="text/xml",
  ...                      contentDisposition='attachment')
  >>> sorted(headers)
  [('Content-Disposition', 'attachment; filename="file"'),
   ('Content-Length', '0'),
   ('Content-Type', 'text/xml')]

The filename provided to the browser can be controlled similarly.  If
the content object provides one, it will be used by default:

  >>> headers = getHeaders(f, contentDisposition='attachment')
  >>> sorted(headers)
  [('Content-Disposition', 'attachment; filename="file"'),
   ('Content-Length', '0'),
   ('Content-Type', 'text/plain')]

Providing an alternate name to ``getHeaders`` overrides the download
name from the file:

  >>> headers = getHeaders(f, downloadName="foo.txt",
  ...                      contentDisposition='attachment')
  >>> sorted(headers)
  [('Content-Disposition', 'attachment; filename="foo.txt"'),
   ('Content-Length', '0'),
   ('Content-Type', 'text/plain')]

The default Content-Disposition header can be overridden by providing
an argument to ``getHeaders``:

  >>> headers = getHeaders(f, contentDisposition="inline")
  >>> sorted(headers)
  [('Content-Disposition', 'inline; filename="file"'),
   ('Content-Length', '0'),
   ('Content-Type', 'text/plain')]

If the ``contentDisposition`` argument is not provided, none will be
included in the headers:

  >>> headers = getHeaders(f)
  >>> sorted(headers)
  [('Content-Length', '0'),
   ('Content-Type', 'text/plain')]


Body
====

We use DownloadResult to deliver the content to the browser.  Since
there's no data in this file, there are no body chunks:

  >>> transaction.commit()
  >>> from zope.file.download import DownloadResult
  >>> result = DownloadResult(f)
  >>> list(result)
  []

We still need to see how non-empty files are handled.  Let's write
some data to our file object:

  >>> with f.open("w") as w:
  ...    _ = w.write(b"some text")
  ...    w.flush()
  >>> transaction.commit()

Now we can create a result object and see if we get the data we
expect:

  >>> result = DownloadResult(f)
  >>> L = list(result)
  >>> b"".join(L)
  b'some text'

If the body content is really large, the iterator may provide more
than one chunk of data:

  >>> with f.open("w") as w:
  ...   _ = w.write(b"*" * 1024 * 1024)
  ...   w.flush()
  >>> transaction.commit()

  >>> result = DownloadResult(f)
  >>> L = list(result)
  >>> len(L) > 1
  True

Once iteration over the body has completed, further iteration will not
yield additional data:

  >>> list(result)
  []


The Download View
=================

Now that we've seen the ``getHeaders`` function and the result object,
let's take a look at the basic download view that uses them.  We'll need
to add a file object where we can get to it using a browser:

  >>> f = File()
  >>> f.mimeType = "text/plain"
  >>> with f.open("w") as w:
  ...    _ = w.write(b"some text")
  >>> transaction.commit()

  >>> getRootFolder()["abcdefg"] = f

  >>> transaction.commit()

Now, let's request the download view of the file object and check the
result:

  >>> print(http(b"""
  ... GET /abcdefg/@@download HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: attachment; filename="abcdefg"
  Content-Length: 9
  Content-Type: text/plain
  <BLANKLINE>
  some text


The Inline View
===============

In addition, it is sometimes useful to view the data inline instead of
downloading it.  A basic inline view is provided for this use case.
Note that browsers may decide not to display the image when this view
is used and there is not page that it's being loaded into: if this
view is being referenced directly via the URL, the browser may show
nothing:

  >>> print(http(b"""
  ... GET /abcdefg/@@inline HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: inline; filename="abcdefg"
  Content-Length: 9
  Content-Type: text/plain
  <BLANKLINE>
  some text


The Default Display View
========================

This view is similar to the download and inline views, but no content
disposition is specified at all.  This lets the browser's default
handling of the data in the current context to be applied:

  >>> print(http(b"""
  ... GET /abcdefg/@@display HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Length: 9
  Content-Type: text/plain
  <BLANKLINE>
  some text

Large Unicode Characters
========================

We need to be able to support Unicode characters in the filename
greater than what Latin-1 (the encoding used by WSGI) can support.

Let's rename a file to contain a high Unicode character and try to
download it; the filename will be encoded:

  >>> getRootFolder()["abcdefg"].__name__ = u'Big \U0001F4A9'
  >>> transaction.commit()

  >>> print(http(b"""
  ... GET /abcdefg/@@download HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: attachment; filename="Big ð©"
  Content-Length: 9
  Content-Type: text/plain
  <BLANKLINE>
  some text
