"""Test setup for integration and functional tests."""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies."""

    fiveconfigure.debug_mode = True
    from collective.geo import contentlocations, kml

    zcml.load_config('configure.zcml', kml)
    zcml.load_config('configure.zcml', contentlocations)

    fiveconfigure.debug_mode = False

    #ztc.installPackage('collective.geo.contentlocations')

setup_product()
ptc.setupPloneSite(products=['collective.geo.kml','collective.geo.contentlocations'])

class ContentlocationsTestCase(ptc.PloneTestCase):
    pass

class ContentlocationsFunctionalTestCase(ptc.FunctionalTestCase):
    pass
