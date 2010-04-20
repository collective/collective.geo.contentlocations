import unittest
from collective.geo.contentlocations.tests import base


class TestSetup(base.TestCase):

    def test_portal_actions(self):
        location_action = self.portal.portal_actions.object.get('locations',
                                                                        False)
        self.failUnless(location_action)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
