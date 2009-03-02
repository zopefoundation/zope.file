##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.file package

$Id: setup.py 80818 2007-10-11 04:06:12Z srichter $
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.file',
      version = '0.5.0dev',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Efficient File Implementation for Zope Applications',
      long_description=(
          read('README.txt')
          + '\n\n' +
          'Detailed Documentation\n' +
          '======================\n\n'
          + '\n\n' +
          read('src', 'zope', 'file', 'README.txt')
          + '\n\n' +
          read('src', 'zope', 'file', 'download.txt')
          + '\n\n' +
          read('src', 'zope', 'file', 'upload.txt')
          + '\n\n' +
          read('src', 'zope', 'file', 'contenttype.txt')
          + '\n\n' +
          read('src', 'zope', 'file', 'browser.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope3 web html ui file pattern",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://cheeseshop.python.org/pypi/zope.file',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      extras_require = dict(
          test=['zope.app.testing',
                'zope.app.securitypolicy',
                'zope.app.zcmlfiles',
                'zope.testbrowser',
                'zope.formlib',
                'zope.app.server']),
     install_requires=['setuptools',
                       'ZODB3',
                       'zope.app.appsetup',
                       'zope.app.container',
                       'zope.app.publication',
                       'zope.app.wsgi',
                       'zope.container',
                       'zope.event',
                       'zope.interface',
                       'zope.publisher',
                       'zope.security',
                       'zope.mimetype',
                       ],
      include_package_data = True,
      zip_safe = False,
      )
