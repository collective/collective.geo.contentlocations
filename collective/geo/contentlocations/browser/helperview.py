import pkg_resources
from Products.Five.browser import BrowserView

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True
    from plone.dexterity.interfaces import IDexterityContent

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.settings.utils import geo_settings


class HelperView(BrowserView):

    def isGeoreferenceable(self):
        geo_contenttypes = geo_settings().geo_content_types
        return (
            IGeoreferenceable.providedBy(self.context) and
            self.context.portal_type in geo_contenttypes)

    def isDexterityContentType(self):
        if HAS_DEXTERITY:
            return IDexterityContent.providedBy(self.context)
        return False

    def showCoordinatesTab(self):
        # Dexterity content types don't need Coordinates Tab
        return self.isGeoreferenceable() and not self.isDexterityContentType()
