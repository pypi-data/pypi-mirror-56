from plone.testing import Layer
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from zope.component import getMultiAdapter
import collective.noindexing
import pkg_resources

try:
    pkg_resources.get_distribution("plone.app.contenttypes")
except pkg_resources.DistributionNotFound:
    GS_PROFILE_ID=None
else:
    GS_PROFILE_ID="plone.app.contenttypes:default"

NOINDEXING_FIXTURE = PloneWithPackageLayer(
        name="NOINDEXING_FIXTURE",
        zcml_package=collective.noindexing,
        zcml_filename="testing.zcml",
        gs_profile_id=GS_PROFILE_ID)
NOINDEXING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOINDEXING_FIXTURE,), name="NoIndexing:Integration")


class NoIndexingAppliedLayer(Layer):

    def testSetUp(self):
        from collective.noindexing import patches
        patches.apply()

    def testTearDown(self):
        from collective.noindexing import patches
        patches.unapply()


NOINDEXING_APPLIED_FIXTURE = NoIndexingAppliedLayer(
        bases=(NOINDEXING_FIXTURE,),
        name="NOINDEXING_APPLIED_FIXTURE")
NOINDEXING_APPLIED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOINDEXING_APPLIED_FIXTURE,), name="NoIndexingApplied:Integration")


def make_test_doc(portal, suffix=""):
    new_id = "document-coll-noindexing" + suffix
    portal.invokeFactory('Document', new_id)
    doc = portal[new_id]
    doc.reindexObject()  # Might have already happened, but let's be sure.
    return doc


def apply_patches(portal):
    """Apply patches.

    We could just do this:

    from collective.noindexing import patches
    patches.apply()

    But it is good to use the browser view here.
    """
    view = getMultiAdapter((portal, portal.REQUEST),
                           name='collective-noindexing-apply')
    view()


def unapply_patches(portal):
    view = getMultiAdapter((portal, portal.REQUEST),
                           name='collective-noindexing-unapply')
    view()
