##############################################################################
#
# Copyright (c) 2006-2009 Zope Corporation and Contributors.
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

"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

version = '1.0.0'

setup(
    name='zope.file',
    version=version,
    author='Zope Corporation and Contributors',
    author_email='zope-dev@zope.org',
    description='Efficient File Implementation for Zope Applications',
    long_description=(
        read('README.rst')
        + '\n\n' +
        '.. contents::'
        + '\n\n' +
        read('src', 'zope', 'file', 'README.rst')
        + '\n\n' +
        read('src', 'zope', 'file', 'download.rst')
        + '\n\n' +
        read('src', 'zope', 'file', 'upload.rst')
        + '\n\n' +
        read('src', 'zope', 'file', 'contenttype.rst')
        + '\n\n' +
        read('src', 'zope', 'file', 'browser.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    keywords="zope3 web html ui file pattern",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python:: 2',
        'Programming Language :: Python:: 2.7',
        'Programming Language :: Python:: 3',
        'Programming Language :: Python:: 3.4',
        'Programming Language :: Python:: 3.5',
        'Programming Language :: Python:: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3',
    ],
    url='http://cheeseshop.python.org/pypi/zope.file',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope'],
    extras_require=dict(
        test=[
            'zope.app.basicskin >= 4.0.0',
            'zope.app.http',
            'zope.app.pagetemplate >= 4.0.0',
            'zope.app.principalannotation',
            'zope.app.publication',
            'zope.app.wsgi',

            'zope.applicationcontrol',
            'zope.copypastemove',
            'zope.browser',
            'zope.browsermenu',
            'zope.login',
            'zope.password',
            'zope.proxy >= 4.2.1',
            'zope.principalregistry',
            'zope.securitypolicy',
            'zope.testbrowser >= 5.2',
            'zope.testrunner',
        ],
        browser=[
            'zope.browser',
        ]
    ),
    install_requires=[
        'setuptools',
        'ZODB',
        'zope.component',
        'zope.container',
        'zope.contenttype',
        'zope.event',
        'zope.filerepresentation',
        'zope.formlib',
        'zope.i18nmessageid',
        'zope.lifecycleevent',
        'zope.interface',
        'zope.location',
        'zope.mimetype >= 2.2',
        'zope.publisher >= 4.3.1',
        'zope.schema',
        'zope.security >= 4.1.0',
        'zope.size',
    ],
    include_package_data=True,
    zip_safe=False,
)
