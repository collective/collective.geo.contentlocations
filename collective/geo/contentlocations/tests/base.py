"""Test setup for integration and functional tests."""
from AccessControl.SecurityManager import setSecurityPolicy
from AccessControl.ImplPython import ZopeSecurityPolicy
from zope.component import provideAdapter
from zope.component import eventtesting

# from Products.Five import zcml
from Zope2.App import zcml
from Products.Five import fiveconfigure
from Products.Five.testbrowser import Browser

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
ptc.setupPloneSite(
        extension_profiles=('collective.geo.contentlocations:default', ))


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

        #Set up our security policy so we can get verbose errors, if any
        setSecurityPolicy(ZopeSecurityPolicy(verbose=True))

        #Make sure our test browser won't try to handle errors
        self.browser = Browser()
        self.browser.handleErrors = False

        #Make our portal error log ignore no exceptions
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):  # pylint: disable=W0613
            print info[1]

        #Make sure our site error log raises errors so we can check for them
        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()
        # unregister IGeoCustomFeatureStyle adapter
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(GeoStyleManager, (IGeoreferenceable, ),
                                                IGeoCustomFeatureStyle)
