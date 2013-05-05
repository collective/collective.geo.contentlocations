from Products.Five.browser import BrowserView
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.settings.utils import geo_settings
from .. import utils


class HelperView(BrowserView):

    def isGeoreferenceable(self):
        geo_contenttypes = geo_settings().geo_content_types
        return (
            IGeoreferenceable.providedBy(self.context) and
            self.context.portal_type in geo_contenttypes)

    def isDexterityContentType(self):
        return utils.isDexterityContentType(self.context)

    def showCoordinatesTab(self):
        # Dexterity content types don't need Coordinates Tab
        return self.isGeoreferenceable() and not self.isDexterityContentType()
