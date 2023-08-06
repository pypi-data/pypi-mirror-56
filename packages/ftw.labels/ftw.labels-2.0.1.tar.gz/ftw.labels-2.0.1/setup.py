import os
from setuptools import setup, find_packages


version = '2.0.1'


tests_require = [
    'asserts',
    'ftw.builder',
    'ftw.testbrowser',
    'ftw.testing>=2',
    'plone.app.testing',
    'plone.mocktestcase',
    'transaction',
    'zope.configuration'
    ]


setup(name='ftw.labels',
      version=version,
      description='A Plone addon for labels.',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw labels',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.labels',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Acquisition',
        'Plone',
        'Products.CMFCore',
        'Products.GenericSetup',
        'ZODB3',
        'Zope2',
        'plone.api',
        'plone.app.portlets',
        'plone.i18n',
        'plone.indexer',
        'plone.portlets',
        'setuptools',
        'z3c.json',
        'zExceptions',
        'zope.annotation',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
