import unittest

from ..testing import CGEO_CONTENTLOCATIONS_FUNCTIONAL


class TestSetup(unittest.TestCase):

    layer = CGEO_CONTENTLOCATIONS_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']

    def test_portal_actions(self):
        pa = self.portal.portal_actions
        location_action = pa.object.get('locations', False)
        self.failUnless(location_action)
