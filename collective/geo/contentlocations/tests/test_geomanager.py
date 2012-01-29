import unittest
import doctest
import collective.geo.contentlocations.geomanager

import zope.component
import collective.geo.geographer.geo
import collective.geo.geographer.interfaces
import zope.annotation.interfaces
import zope.annotation.attribute


def setUp(test):

    zope.component.provideAdapter(
            collective.geo.geographer.geo.GeoreferencingAnnotator,
            provides=collective.geo.geographer.interfaces.IWriteGeoreferenced
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
                     optionflags=doctest.NORMALIZE_WHITESPACE | \
                                                doctest.ELLIPSIS,
                    ),
        ))
