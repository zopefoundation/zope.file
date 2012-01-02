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
"""The 'Content Type' view for files.

"""
__docformat__ = "reStructuredText"

import zope.component
import zope.formlib.form
import zope.formlib.interfaces
import zope.interface
import zope.lifecycleevent
import zope.mimetype.event
import zope.mimetype.interfaces
import zope.mimetype.source
import zope.schema
import zope.security.proxy

from zope import mimetype
from zope.file.i18n import _


def validateCodecUse(file, iface, codec, codec_field):
    """Validate the use of `codec` for the data in `file`.

    `iface` is used as the content-type interface for `file`.  If
    `iface` is None, no validation is performed and no error is
    reported (this validation is considered irrelevant).

    If `codec` is None, no error is reported, since that indicates
    that no codec is known to be accurate for the data in `file`.

    `codec_field` is the form field that is used to select the codec;
    it is used to generate an error should one be necessary.

    Returns a list of widget input errors that should be added to any
    other errors the form determines are relevant.

    """
    errs = []
    if (codec is not None) and (iface is not None):
        if iface.extends(mimetype.interfaces.IContentTypeEncoded):
            # Need to test that this codec can be used for this
            # document:
            f = file.open("r")
            content_data = f.read()
            f.close()
            try:
                text, consumed = codec.decode(content_data)
                if consumed != len(content_data):
                    raise UnicodeError("not all data decoded")
            except UnicodeError:
                err = zope.formlib.interfaces.WidgetInputError(
                    codec_field.__name__,
                    codec_field.field.title,
                    "Selected encoding cannot decode document.")
                errs.append(err)
    return errs


class ContentTypeForm(zope.formlib.form.Form):

    mimeType_field = zope.formlib.form.Field(
        zope.schema.Choice(
            __name__="mimeType",
            title=_("Content type"),
            description=_("Type of document"),
            source=mimetype.source.contentTypeSource,
            ))

    encoding_field = zope.formlib.form.Field(
        zope.schema.Choice(
            __name__="encoding",
            title=_("Encoding"),
            description=_("Character data encoding"),
            source=mimetype.source.codecSource,
            required=False,
            ))

    def get_rendered_encoding(self):
        charset = self.context.parameters.get("charset")
        if charset:
            return zope.component.queryUtility(
                mimetype.interfaces.ICharsetCodec, charset)
        else:
            return None
    encoding_field.get_rendered = get_rendered_encoding

    def get_rendered_mimeType(self):
        # make sure we return the exact `IContentType`-derived
        # interface that the context provides; there *must* be only
        # one!
        ifaces = zope.interface.directlyProvidedBy(
            zope.security.proxy.removeSecurityProxy(self.context))
        for iface in ifaces:
            if mimetype.interfaces.IContentTypeInterface.providedBy(iface):
                return iface
        return None
    mimeType_field.get_rendered = get_rendered_mimeType

    def setUpWidgets(self, ignore_request=False):
        # We need to re-compute the fields before initializing the widgets
        fields = [self.mimeType_field]
        if mimetype.interfaces.IContentTypeEncoded.providedBy(self.context):
            self.have_encoded = True
            fields.append(self.encoding_field)
        else:
            self.have_encoded = False
        self.form_fields = zope.formlib.form.Fields(*fields)
        super(ContentTypeForm, self).setUpWidgets(
            ignore_request=ignore_request)

    def save_validator(self, action, data):
        errs = self.validate(None, data)
        errs += validateCodecUse(
            self.context, data.get("mimeType"), data.get("encoding"),
            self.encoding_field)
        return errs

    @zope.formlib.form.action(_("Save"), validator=save_validator)
    def save(self, action, data):
        context = self.context
        if data.get("mimeType"):
            #
            # XXX Note that the content type parameters are not
            # modified; ideally, the IContentInfo adapter would filter
            # the parameters for what makes sense for the current
            # content type.
            #
            iface = data["mimeType"]
            unwrapped = zope.security.proxy.removeSecurityProxy(context)
            mimetype.event.changeContentType(unwrapped, iface)

        # update the encoding, but only if the new content type is encoded
        encoded = mimetype.interfaces.IContentTypeEncoded.providedBy(
            context)
        # We only care about encoding if we're encoded now and were also
        # encoded before starting the re
        if encoded and self.have_encoded:
            codec = data["encoding"]
            if codec is None:
                # remove any charset found, since the user said it was wrong;
                # what it means to have no known charset is that the policy
                # (IContentInfo) will have to decide how to treat encoding.
                if "charset" in context.parameters:
                    # We can't just "del" the existing value, since
                    # the security model does not like that.  We can
                    # set a new value for context.parameters, though.
                    parameters = dict(context.parameters)
                    del parameters["charset"]
                    context.parameters = parameters
            else:
                if "charset" in context.parameters:
                    old_codec = zope.component.queryUtility(
                        mimetype.interfaces.ICharsetCodec,
                        context.parameters["charset"])
                else:
                    old_codec = None
                if getattr(old_codec, "name", None) != codec.name:
                    # use the preferred charset for the new codec
                    new_charset = zope.component.getUtility(
                        mimetype.interfaces.ICodecPreferredCharset,
                        codec.name)
                    parameters = dict(context.parameters)
                    parameters["charset"] = new_charset.name
                    context.parameters = parameters
        zope.event.notify(
            zope.lifecycleevent.ObjectModifiedEvent(
                zope.security.proxy.removeSecurityProxy(context)))
