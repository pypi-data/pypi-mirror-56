from setuptools import setup, find_packages

version = '2.0.0'

setup(name='collective.noindexing',
      version=version,
      description="Ignore all indexing operations",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from https://pypi.org/classifiers/
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.1",
          "Framework :: Plone :: 5.2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          ],
      keywords='catalog index plone',
      author='Maurits van Rees',
      author_email='m.van.rees@zestsoftware.nl',
      url='https://github.com/collective/collective.noindexing',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFCore',
      ],
      extras_require={
          'test': ['plone.app.testing',
                   'unittest2',
                   'zope.configuration',
                   'zope.component'],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
