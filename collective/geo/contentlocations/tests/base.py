"""Test setup for integration and functional tests."""
from zope.component import provideAdapter
from Products.CMFCore.PortalContent import PortalContent

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.contentlocations.geostylemanager import GeoStyleManager


@onsetup
def setup_product():
    """Set up the package and its dependencies."""

    fiveconfigure.debug_mode = True
    from collective.geo import contentlocations

    zcml.load_config('configure.zcml', contentlocations)

    fiveconfigure.debug_mode = False


setup_product()
ptc.setupPloneSite(products=['collective.geo.contentlocations', ])


class TestCase(ptc.PloneTestCase):
    pass


class FunctionalTestCase(ptc.FunctionalTestCase):

    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()
        # register adapter for custom styles
        provideAdapter(GeoStyleManager, (PortalContent,), IGeoCustomFeatureStyle)

    def tearDown(self):
        # unregister IGeoCustomFeatureStyle adapter
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(GeoStyleManager, (PortalContent,), IGeoCustomFeatureStyle) 
