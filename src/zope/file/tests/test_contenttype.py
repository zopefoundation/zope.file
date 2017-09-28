

import unittest

from zope import component
from zope.interface import implementer

from zope.mimetype.interfaces import IContentTypeEncoded
from zope.mimetype.interfaces import ICodecPreferredCharset

from zope.file.tests import skipWithoutZopeFormlib

@skipWithoutZopeFormlib
class TestCodec(unittest.TestCase):

    def test_unicode_error_too_short(self):
        from zope.file.contenttype import ContentTypeForm
        from zope.file.contenttype import validateCodecUse
        class MockFile(object):
            def open(self, _mode):
                return self

            def read(self):
                return b"Some Data"

            def close(self):
                pass

        class MockCodec(object):
            def decode(self, data):
                return '', 0

        class MockIface(IContentTypeEncoded):
            pass


        errs = validateCodecUse(MockFile(), MockIface,
                                MockCodec(), ContentTypeForm.encoding_field)

        self.assertEqual(1, len(errs))
        self.assertEqual("Selected encoding cannot decode document.",
                         errs[0].errors)

@skipWithoutZopeFormlib
class TestContentTypeForm(unittest.TestCase):

    def test_del_charset_no_encoding(self):
        from zope.file.contenttype import ContentTypeForm
        @implementer(IContentTypeEncoded)
        class MockContext(object):
            def __init__(self):
                self.parameters = {}

        context = MockContext()
        context.parameters['charset'] = "INVALID"

        form = ContentTypeForm(context, None)

        form.have_encoded = True
        data = {}
        data['encoding'] = None

        form.save.success_handler(form, "action", data)
        self.assertNotIn('charset', context.parameters)

    def test_charset_with_encoding(self):
        from zope.file.contenttype import ContentTypeForm
        @implementer(IContentTypeEncoded)
        class MockContext(object):
            def __init__(self):
                self.parameters = {}

        class MockCodec(object):
            name = 'TestContentTypeForm'

        context = MockContext()
        context.parameters['charset'] = "INVALID"

        form = ContentTypeForm(context, None)

        form.have_encoded = True
        data = {}
        codec = data['encoding'] = MockCodec()

        component.provideUtility(codec, ICodecPreferredCharset, codec.name)
        try:
            form.save.success_handler(form, "action", data)
            self.assertIn('charset', context.parameters)
            self.assertEqual(codec.name, context.parameters['charset'])
        finally:
            component.getGlobalSiteManager().unregisterUtility(codec,
                                                               ICodecPreferredCharset, codec.name)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
