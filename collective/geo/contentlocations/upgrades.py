from zope.component.hooks import getSite
from zope.component import getGlobalSiteManager

default_profile = 'profile-collective.geo.contentlocations:default'


def upgrade_to_26(context):
    """this upgrade step fixes browserlayer and Coordinates tab
    and remove all components related to IGeoMarker event
    """
    context.runImportStepFromProfile(default_profile, 'browserlayer')
    context.runImportStepFromProfile(default_profile, 'actions')
    portal = getSite()
    sm = portal.getSiteManager()

    remove_utility = True
    try:
        from .interfaces import IGeoMarkerUtility
    except ImportError:
        remove_utility = False

    if remove_utility:
        util = sm.queryUtility(IGeoMarkerUtility)
        sm.unregisterUtility(provided=IGeoMarkerUtility)
        del util
        assert sm.queryUtility(IGeoMarkerUtility) is None
