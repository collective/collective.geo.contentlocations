import unittest
from collective.geo.contentlocations.tests import base


class TestSetup(base.TestCase):

    def test_portal_actions(self):
        pa = self.portal.portal_actions
        location_action = pa.object.get('locations', False)
        self.failUnless(location_action)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
