import unittest
import doctest
import collective.geo.contentlocations.geomanager
from plone.testing import layered

from ..testing import CGEO_CONTENTLOCATIONS_FUNCTIONAL


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocTestSuite(collective.geo.contentlocations.geomanager),
            layer=CGEO_CONTENTLOCATIONS_FUNCTIONAL),
    ])
    return suite




# import zope.component
# import collective.geo.geographer.geo
# import collective.geo.geographer.interfaces
# import zope.annotation.interfaces
# import zope.annotation.attribute


# def setUp(test):

#     zope.component.provideAdapter(
#             collective.geo.geographer.geo.GeoreferencingAnnotator,
#             provides=collective.geo.geographer.interfaces.IWriteGeoreferenced
#         )

#     zope.component.provideAdapter(
#             zope.annotation.attribute.AttributeAnnotations,
#             provides=zope.annotation.interfaces.IAnnotations
#         )


# def tearDown(test):
#     """This is the companion to setUp - it can be used to clean up the
#     test environment after each test.
#     """
