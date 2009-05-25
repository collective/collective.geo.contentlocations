import unittest
import doctest

from zope.testing import doctestunit
from Testing import ZopeTestCase as ztc

from collective.geo.contentlocations.tests import base

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.txt', package='collective.geo.contentlocations',
            test_class=base.ContentlocationsFunctionalTestCase,
            ),

        ])