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
"""Functional tests for zope.file.

"""
__docformat__ = "reStructuredText"

import doctest
import os.path
import shutil
import tempfile

import transaction
from ZODB.DB import DB
from ZODB.DemoStorage import DemoStorage
from ZODB.blob import BlobStorage
import zope.app.testing.functional
from zope.app.component.hooks import setSite
import ZODB.interfaces

here = os.path.dirname(os.path.realpath(__file__))

class FunctionalBlobTestSetup(zope.app.testing.functional.FunctionalTestSetup):

    temp_dir_name = None
    direct_blob_support = False

    def setUp(self):
        """Prepares for a functional test case."""
        # Tear down the old demo storage (if any) and create a fresh one
        transaction.abort()
        self.db.close()
        storage = DemoStorage("Demo Storage", self.base_storage)
        if ZODB.interfaces.IBlobStorage.providedBy(storage):
            # at least ZODB 3.9
            self.direct_blob_support = True
        else:
            # make a dir
            temp_dir_name = self.temp_dir_name = tempfile.mkdtemp()
            # wrap storage with BlobStorage
            storage = BlobStorage(temp_dir_name, storage)
        self.db = self.app.db = DB(storage)
        self.connection = None

    def tearDown(self):
        """Cleans up after a functional test case."""
        transaction.abort()
        if self.connection:
            self.connection.close()
            self.connection = None
        self.db.close()
        if not self.direct_blob_support and self.temp_dir_name is not None:
            # del dir named '__blob_test__%s' % self.name
            shutil.rmtree(self.temp_dir_name, True)
            self.temp_dir_name = None
        setSite(None)

class ZCMLLayer(zope.app.testing.functional.ZCMLLayer):

    def setUp(self):
        self.setup = FunctionalBlobTestSetup(self.config_file)

def FunctionalBlobDocFileSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['http'] = zope.app.testing.functional.HTTPCaller()
    globs['getRootFolder'] = zope.app.testing.functional.getRootFolder
    globs['sync'] = zope.app.testing.functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        FunctionalBlobTestSetup().setUp()

        if kwsetUp is not None:
            kwsetUp(test)
    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        if kwtearDown is not None:
            kwtearDown(test)
        FunctionalBlobTestSetup().tearDown()
    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.REPORT_NDIFF
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = zope.app.testing.functional.Functional
    return suite

ZopeFileLayer = ZCMLLayer(
    os.path.join(here, "ftesting.zcml"), __name__, "ZopeFileLayer")
