======================
 Uploading a new file
======================

There's a simple view for uploading a new file.  Let's try it:

  >>> from io import BytesIO as StringIO

  >>> sio = StringIO(b"some text")

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.addHeader("Authorization", "Basic mgr:mgrpw")
  >>> browser.addHeader("Accept-Language", "en-US")

  >>> browser.open("http://localhost/@@+/zope.file.File")

  >>> ctrl = browser.getControl(name="form.data")
  >>> ctrl.add_file(
  ...     sio, "text/plain; charset=utf-8", "plain.txt")
  >>> browser.getControl("Add").click()

Now, let's request the download view of the file object and check the
result:

  >>> print(http(b"""
  ... GET /plain.txt/@@download HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: attachment; filename="plain.txt"
  Content-Length: 9
  Content-Type: text/plain;charset=utf-8
  <BLANKLINE>
  some text

We'll peek into the database to make sure the object implements the
expected MIME type interface:

  >>> from zope.mimetype import types
  >>> ob = getRootFolder()["plain.txt"]
  >>> types.IContentTypeTextPlain.providedBy(ob)
  True

We can upload new data into our file object as well:

  >>> sio = StringIO(b"new text")
  >>> browser.open("http://localhost/plain.txt/@@edit.html")

  >>> ctrl = browser.getControl(name="form.data")
  >>> ctrl.add_file(
  ...     sio, "text/plain; charset=utf-8", "stuff.txt")
  >>> browser.getControl("Edit").click()

Now, let's request the download view of the file object and check the
result:

  >>> print(http(b"""
  ... GET /plain.txt/@@download HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: attachment; filename="plain.txt"
  Content-Length: 8
  Content-Type: text/plain;charset=utf-8
  <BLANKLINE>
  new text

If we upload a file that has imprecise content type information (as we
expect from browsers generally, and MSIE most significantly), we can
see that the MIME type machinery will improve the information where
possible:

  >>> sio = StringIO(b"<?xml version='1.0' encoding='utf-8'?>\n"
  ...                b"<html>...</html>\n")

  >>> browser.open("http://localhost/@@+/zope.file.File")

  >>> ctrl = browser.getControl(name="form.data")
  >>> ctrl.add_file(
  ...     sio, "text/html; charset=utf-8", "simple.html")
  >>> browser.getControl("Add").click()

Again, we'll request the download view of the file object and check
the result:

  >>> print(http(b"""
  ... GET /simple.html/@@download HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: attachment; filename="simple.html"
  Content-Length: 56
  Content-Type: application/xhtml+xml;charset=utf-8
  <BLANKLINE>
  <?xml version='1.0' encoding='utf-8'?>
  <html>...</html>
  <BLANKLINE>

Further, if a browser is bad and sends a full path as the file name (as
sometimes happens in many browsers, apparently), the name is correctly
truncated and changed.

  >>> sio = StringIO(b"<?xml version='1.0' encoding='utf-8'?>\n"
  ...                b"<html>...</html>\n")

  >>> browser.open("http://localhost/@@+/zope.file.File")

  >>> ctrl = browser.getControl(name="form.data")
  >>> ctrl.add_file(
  ...     sio, "text/html; charset=utf-8", r"C:\Documents and Settings\Joe\naughty name.html")
  >>> browser.getControl("Add").click()


Again, we'll request the download view of the file object and check
the result:

  >>> print(http(b"""
  ... GET /naughty%20name.html/@@download HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Disposition: attachment; filename="naughty name.html"
  Content-Length: 56
  Content-Type: application/xhtml+xml;charset=utf-8
  <BLANKLINE>
  <?xml version='1.0' encoding='utf-8'?>
  <html>...</html>
  <BLANKLINE>

In zope.file <= 0.5.0, a redundant ObjectCreatedEvent was fired in the
Upload view.  We'll demonstrate that this is no longer the case.

  >>> import zope.component
  >>> from zope.file.interfaces import IFile
  >>> from zope.lifecycleevent import IObjectCreatedEvent

We'll register a subscriber for IObjectCreatedEvent that simply increments
a counter.

  >>> count = 0
  >>> def inc(*args):
  ...   global count; count += 1
  >>> zope.component.provideHandler(inc, (IFile, IObjectCreatedEvent))

  >>> browser.open("http://localhost/@@+/zope.file.File")

  >>> ctrl = browser.getControl(name="form.data")
  >>> sio = StringIO(b"some data")
  >>> ctrl.add_file(
  ...     sio, "text/html; charset=utf-8", "name.html")
  >>> browser.getControl("Add").click()

The subscriber was called only once.

  >>> print(count)
  1
