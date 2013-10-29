import unittest
import doctest

from plone.testing import layered
from ..testing import CGEO_CONTENTLOCATIONS_FUNCTIONAL


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'README.txt',
                package='collective.geo.contentlocations'),
            layer=CGEO_CONTENTLOCATIONS_FUNCTIONAL),
        layered(
            doctest.DocFileSuite(
                'geostylemanager.txt',
                package='collective.geo.contentlocations'),
            layer=CGEO_CONTENTLOCATIONS_FUNCTIONAL)
    ])
    return suite
