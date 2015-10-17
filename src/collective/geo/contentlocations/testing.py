# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile

import collective.geo.contentlocations


class CGeoContentLocationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.geo.geographer
        self.loadZCML(package=collective.geo.geographer)
        import collective.geo.behaviour
        self.loadZCML(package=collective.geo.behaviour)
        self.loadZCML(package=collective.geo.contentlocations)

    def setUpPloneSite(self, portal):
        """ do special site setup here"""
        applyProfile(portal, 'collective.geo.contentlocations:default')


CGEO_CONTENTLOCATIONS = CGeoContentLocationsLayer()

CGEO_CONTENTLOCATIONS_INTEGRATION = IntegrationTesting(
    bases=(CGEO_CONTENTLOCATIONS, ),
    name="CGEO_CONTENTLOCATIONS_INTEGRATION")

CGEO_CONTENTLOCATIONS_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_CONTENTLOCATIONS, ),
    name="CGEO_CONTENTLOCATIONS_FUNCTIONAL")
