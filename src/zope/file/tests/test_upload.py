

import unittest

from zope import component
from zope.interface import implementer

from zope.file import upload

from zope.mimetype.interfaces import IContentTypeEncoded
from zope.mimetype.interfaces import ICharsetCodec
from zope.mimetype.interfaces import ICodecPreferredCharset
from zope.mimetype.interfaces import IMimeTypeGetter

from zope.mimetype.typegetter import smartMimeTypeGuesser

from io import BytesIO

@implementer(IContentTypeEncoded)
class MockContext(object):
    def __init__(self):
        self.parameters = {}

    def open(self, _):
        return self

    def write(self, _):
        pass

    def close(self):
        pass


class TestFunctions(unittest.TestCase):

    def test_name_finder_with_no_filename(self):

        class MockFile(object):
            pass

        res = upload.nameFinder(MockFile())

        self.assertIsNone(res)

class TestUpdateBlob(unittest.TestCase):

    def setUp(self):
        super(TestUpdateBlob, self).setUp()
        component.provideUtility(smartMimeTypeGuesser, IMimeTypeGetter)
        self.context = MockContext()
        self.data = BytesIO()
        self.data.headers = {}

    def tearDown(self):
        gsm = component.getGlobalSiteManager()
        gsm.unregisterUtility(smartMimeTypeGuesser, IMimeTypeGetter)
        super(TestUpdateBlob, self).tearDown()

    def test_no_mime_type(self):
        upload.updateBlob(self.context, self.data)
        self.assertEqual(self.context.mimeType, 'application/octet-stream')
        self.assertEqual(self.context.parameters, {})

class TestReupload(unittest.TestCase):

    def test_different_codec(self):

        class MockCodec(object):
            name = 'TestContentTypeForm'

        class MockRequest(object):
            form = ()
            headers = ()

        context = MockContext()
        orig_codec_name = context.parameters['charset'] = 'Original'

        request = MockRequest()
        form = upload.Reupload(context, request)

        sio = BytesIO()
        request.form = {'form.data': sio}
        sio.headers = {'Content-Type': 'text/plain; charset=TestContentTypeForm'}

        form.have_encoded = True
        data = {}
        codec = data['encoding'] = MockCodec()

        data['data'] = 1

        orig_codec = MockCodec()
        orig_codec.name = orig_codec_name

        component.provideUtility(orig_codec, ICharsetCodec, orig_codec_name)
        component.provideUtility(codec, ICharsetCodec, codec.name.lower())
        component.provideUtility(codec, ICodecPreferredCharset, codec.name)
        component.provideUtility(smartMimeTypeGuesser, IMimeTypeGetter)
        try:
            form.upload.success_handler(form, "action", data)
            self.assertIn('charset', context.parameters)
            self.assertEqual(codec.name, context.parameters['charset'])
        finally:
            gsm = component.getGlobalSiteManager()
            gsm.unregisterUtility(codec,
                                  ICodecPreferredCharset, codec.name.lower())
            gsm.unregisterUtility(orig_codec, ICharsetCodec, orig_codec_name)
            gsm.unregisterUtility(smartMimeTypeGuesser, IMimeTypeGetter)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
