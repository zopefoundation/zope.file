=========
 CHANGES
=========

1.2.1 (unreleased)
==================

- Add support for Python 3.9, 3.10.


1.2.0 (2020-03-06)
==================

- Add support for Python 3.7 and 3.8.

- Drop Python 3.4 support.


1.1.0 (2017-09-30)
==================

- Move more browser dependencies to the ``browser`` extra.

- Begin testing PyPy3 on Travis CI.


1.0.0 (2017-04-25)
==================

- Remove unneeded test dependencies zope.app.server,
  zope.app.component, zope.app.container, and others.

- Update to work with zope.testbrowser 5.

- Add PyPy support.

- Add support for Python 3.4, 3.5 and 3.6.
  See `PR 5 <https://github.com/zopefoundation/zope.file/pull/5>`_.

0.6.2 (2012-06-04)
==================

- Moved menu-oriented registrations into new menus.zcml. This is now
  loaded if zope.app.zcmlfiles is available only.

- Increase test coverage.

0.6.1 (2012-01-26)
==================

- Declared more dependencies.


0.6.0 (2010-09-16)
==================

- Bug fix: remove duplicate firing of ObjectCreatedEvent in
  zope.file.upload.Upload (the event is already fired in its base class,
  zope.formlib.form.AddForm).

- Move browser-related zcml to `browser.zcml` so that it easier for
  applications to exclude it.

- Import content-type parser from zope.contenttype, adding a dependency on
  that package.

- Removed undeclared dependency on zope.app.container, depend on zope.browser.

- Using Python's ``doctest`` module instead of deprecated
  ``zope.testing.doctest``.

0.5.0 (2009-07-23)
==================

- Change package's mailing list address to zope-dev at zope.org instead
  of the retired one.

- Made tests compatible with ZODB 3.9.

- Removed not needed install requirement declarations.


0.4.0 (2009-01-31)
==================

- `openDetached` is now protected by zope.View instead of zope.ManageContent.

- Use zope.container instead of zope.app.container.

0.3.0 (2007-11-01)
==================

- Package data update.

0.2.0 (2007-04-18)
==================

- Fix code for Publisher version 3.4.

0.1.0 (2007-04-18)
==================

- Initial release.
