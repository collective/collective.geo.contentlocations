from zope.interface import Interface

from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations import config
from collective.geo.geopoint.interfaces import IGeoPoint
from zope import schema

class IGeoView(Interface):
    """ View to access coordinates """
    def isGeoreferenceable():
        """Returns True if an object is Georeferenceable"""

    def getCoordinates(self):
        """ Public function to get object coordinates """


class IGeoForm(Interface):
    """ Interface for coordinates management forms """

class IGeoManager(IGeoPoint):
    """ Interface for point management """
    coord_type = schema.Choice(title=_(u"Type"),
                               description=_(u"Choose type of coordinates."),
                               vocabulary = 'coordsVocab',
                               #values=config.COORDTYPE,
                               required=True )

    filecsv = schema.Bytes(title=_(u"File")) 

    def isGeoreferenceable(self):
        """ """
    def getCoordinates(self):
        """ """
    def setCoordinates(self):
        """ """

