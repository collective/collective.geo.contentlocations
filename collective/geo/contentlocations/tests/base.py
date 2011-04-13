"""Test setup for integration and functional tests."""
from zope.component import provideAdapter
from zope.component import eventtesting

# from Products.Five import zcml
from Zope2.App import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.contentlocations.geostylemanager import GeoStyleManager
from collective.geo.geographer.interfaces import IGeoreferenceable


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

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        eventtesting.setUp()

    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()
        # register adapter for custom styles
        provideAdapter(GeoStyleManager, (IGeoreferenceable, ),
                                        IGeoCustomFeatureStyle)

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()
        # unregister IGeoCustomFeatureStyle adapter
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(GeoStyleManager, (IGeoreferenceable, ),
                                                IGeoCustomFeatureStyle)
