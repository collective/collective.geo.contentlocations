import unittest
from zope.testing import doctest, doctestunit
from collective.geo.contentlocations.tests import base
import collective.geo.contentlocations.geomanager

import zope.component
import zgeo.geographer.geo
import zgeo.geographer.interfaces
import zope.annotation.interfaces
import zope.annotation.attribute

def setUp(test):

    zope.component.provideAdapter(
            zgeo.geographer.geo.GeoreferencingAnnotator,
            provides=zgeo.geographer.interfaces.IWriteGeoreferenced
        )

    zope.component.provideAdapter(
            zope.annotation.attribute.AttributeAnnotations,
            provides=zope.annotation.interfaces.IAnnotations
        )

def tearDown(test):
    """This is the companion to setUp - it can be used to clean up the
    test environment after each test.
    """

def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.contentlocations.geomanager,
                     setUp=setUp,
                     tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))
