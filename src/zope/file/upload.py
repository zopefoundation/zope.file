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
"""Upload view for zope.file objects.

"""
__docformat__ = "reStructuredText"

import re
import zope.container.interfaces
import zope.contenttype.parse
import zope.lifecycleevent
import zope.component
import zope.event
import zope.file.file
import zope.formlib.form
import zope.mimetype.event
import zope.mimetype.interfaces
import zope.schema
import zope.security.proxy

from zope import mimetype

from zope.file.i18n import _

_nameFinder = re.compile(r'(.*[\\/:])?(.+)')

def nameFinder(fileob):
    name = getattr(fileob, 'filename', None)
    if name is None:
        return None
    match  = _nameFinder.match(name)
    if match is not None:
        match = match.group(2)
    return match


class Upload(zope.formlib.form.AddForm):

    form_fields = zope.formlib.form.fields(
        zope.schema.Bytes(
            __name__="data",
            title=_("Upload data"),
            description=_("Upload file"),
            ),
        )

    def create(self, data):
        ob = self._create_instance(data)
        f = self.request.form["form.data"]
        updateBlob(ob, f)
        self._name = nameFinder(f)
        return ob

    def add(self, ob):
        if self._name and self.context.nameAllowed():
            nc = zope.container.interfaces.INameChooser(
                self.context.context)
            name = nc.chooseName(self._name, ob)
            self.context.contentName = name
        res = super(Upload, self).add(ob)
        # We need to slam on an interface based on the effective MIME type;
        # start by getting the IContentInfo for ob:
        ci = mimetype.interfaces.IContentInfo(ob, None)
        if (ci is not None) and ci.effectiveMimeType:
            # we might have *something*
            iface = zope.component.queryUtility(
                mimetype.interfaces.IContentTypeInterface,
                ci.effectiveMimeType)
            if iface is not None:
                mimetype.event.changeContentType(ob, iface)
        return res

    def _create_instance(self, data):
        return zope.file.file.File()


class Reupload(zope.formlib.form.Form):

    form_fields = zope.formlib.form.Fields(
        zope.schema.Bytes(
            __name__="data",
            title=_("Upload data"),
            description=_("Upload file to replace the current data"),
            ),
        )

    @zope.formlib.form.action(_("Edit"))
    def upload(self, action, data):
        context = self.context
        if "charset" in context.parameters:
            old_codec = zope.component.queryUtility(
                mimetype.interfaces.ICharsetCodec,
                context.parameters["charset"])
        else:
            old_codec = None

        if data.get("data") is not None:
            updateBlob(context, self.request.form["form.data"])

        # update the encoding, but only if the new content type is encoded
        encoded = mimetype.interfaces.IContentTypeEncoded.providedBy(
            context)
        if encoded and "charset" in context.parameters:
            codec = zope.component.queryUtility(
                mimetype.interfaces.ICharsetCodec,
                context.parameters["charset"])
            if codec and getattr(old_codec, "name", None) != codec.name:
                # use the preferred charset for the new codec
                new_charset = zope.component.getUtility(
                    mimetype.interfaces.ICodecPreferredCharset,
                    codec.name)
                parameters = dict(context.parameters)
                parameters["charset"] = new_charset.name
                context.parameters = parameters
        # these subscribers generally expect an unproxied object.
        zope.event.notify(
            zope.lifecycleevent.ObjectModifiedEvent(
                zope.security.proxy.removeSecurityProxy(context)))


def updateBlob(ob, input):
    # Bypass the widget machinery for now; we'd rather have a blob
    # widget that exposes the interesting information from the
    # upload.
    f = input
    # We need to seek back since the form machinery has already
    # read all the data :-(
    f.seek(0)
    data = f.read()

    contentType = f.headers.get("Content-Type")
    mimeTypeGetter = zope.component.getUtility(
        mimetype.interfaces.IMimeTypeGetter)
    mimeType = mimeTypeGetter(data=data, content_type=contentType,
                              name=nameFinder(f))
    if not mimeType:
        mimeType = "application/octet-stream"
    if contentType:
        major, minor, parameters = zope.contenttype.parse.parse(
            contentType)
        if "charset" in parameters:
            parameters["charset"] = parameters["charset"].lower()
        ob.mimeType = mimeType
        ob.parameters = parameters
    else:
        ob.mimeType = mimeType
        ob.parameters = {}
    w = ob.open("w")
    w.write(data)
    w.close()
