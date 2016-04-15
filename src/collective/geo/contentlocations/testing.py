# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig
from plone.testing import z2

import collective.geo.contentlocations


class CGeoContentLocationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import Products.ATContentTypes
        xmlconfig.file('configure.zcml',
                       Products.ATContentTypes,
                       context=configurationContext)
        z2.installProduct(app, 'plone.app.blob')
        z2.installProduct(app, 'Products.ATContentTypes')

        import collective.geo.geographer
        self.loadZCML(package=collective.geo.geographer)
        import collective.geo.behaviour
        self.loadZCML(package=collective.geo.behaviour)
        self.loadZCML(package=collective.geo.contentlocations)

    def setUpPloneSite(self, portal):
        """ do special site setup here"""
        applyProfile(portal, 'Products.ATContentTypes:default')
        applyProfile(portal, 'collective.geo.contentlocations:default')


CGEO_CONTENTLOCATIONS = CGeoContentLocationsLayer()

CGEO_CONTENTLOCATIONS_INTEGRATION = IntegrationTesting(
    bases=(CGEO_CONTENTLOCATIONS, ),
    name="CGEO_CONTENTLOCATIONS_INTEGRATION")

CGEO_CONTENTLOCATIONS_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_CONTENTLOCATIONS, ),
    name="CGEO_CONTENTLOCATIONS_FUNCTIONAL")
