from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.contentlocations.interfaces import IGeoView
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements

class GeoView(BrowserView):
    implements(IGeoView)

    def __init__(self, context, request):
        self.geomanager = getMultiAdapter((context, self),  IGeoManager)
        super(GeoView, self).__init__(context, request)

    def isGeoreferenceable(self):
        return self.geomanager.isGeoreferenceable()

    def getCoordinates(self):
        return self.geomanager.getCoordinates()
