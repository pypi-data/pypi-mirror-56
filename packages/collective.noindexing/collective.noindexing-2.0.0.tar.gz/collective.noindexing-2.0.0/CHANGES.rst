Changelog
=========

2.0.0 (2019-11-20)
------------------

- Setup Travis. [gotcha]


2.0.0b1 (2019-11-11)
--------------------

- Removed support for Python 2.6 or lower and Plone 4.2 and lower.  [maurits]

- Added Plone 5 compatibility.  Do not require Archetypes.  [gotcha]


1.4 (2013-03-26)
----------------

- make patching a single index method (index, reindex, unindex) possible
  [maartenkling]


1.3 (2012-09-24)
----------------

- Add more (test) dependencies in setup.py.
  [maurits]

- Moved to https://github.com/collective/collective.noindexing
  [maurits]


1.2 (2012-04-18)
----------------

- Fixed the unapply method so a second apply will work correctly.
  [maurits]

- Added tests with plone.app.testing.
  [maurits]

- Added compatibility with Plone 4.1, by loading Products.CMFCore zcml
  for the permissions.
  [maurits]


1.1 (2011-01-04)
----------------

- Moved most logging to debug level as it quickly becomes noise in
  situations where you most need this package.
  [maurits]


1.0 (2010-04-09)
----------------

- Initial release
