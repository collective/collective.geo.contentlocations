from zope.interface import Interface

from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations import config
from collective.geo.geopoint.interfaces import IGeoPoint
from zope import schema

class IGeoView(Interface):
    """ vista coordinate """
    def isGeoreferenceable():
        """Returns True if an object is Georeferenceable"""

    def getCoordinates(self):
        """ public functions to get object coordinates """


class IGeoForm(Interface):
    """ interfaccia per le form di gestione coordinate """

class IGeoManager(IGeoPoint):
    """ interfaccia per la gestione dei punti """
    coord_type = schema.Choice(title=_(u"Type"),
                               description=_(u"Choose type of coordinates."),
                               values=config.COORDTYPE,
                               required=True )

    filecsv = schema.Bytes(title=_(u"File")) 

    def isGeoreferenceable(self):
        """ """
    def getCoordinates(self):
        """ """
    def setCoordinates(self):
        """ """

