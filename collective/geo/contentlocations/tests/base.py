"""Test setup for integration and functional tests."""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


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
    pass
