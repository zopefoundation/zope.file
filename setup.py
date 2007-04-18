from setuptools import setup, find_packages

setup(
    name="zope.file",
    version="0.3dev",
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['zope'],
    include_package_data=True,
    zip_safe = False,
    install_requires=['setuptools',
                      'zope.app.appsetup',
                      'zope.app.publication',
                      'zope.app.wsgi',
                      'zope.event',
                      'zope.interface',
                      'zope.publisher',
                      'zope.security',
                      'zope.mimetype',
                      # "extras"
                      'zope.app.testing',
                      'zope.app.securitypolicy',
                      'zope.app.zcmlfiles',
                      'zope.testbrowser',
                      'zope.formlib',
                      'zope.app.server',
                      ],
    )
