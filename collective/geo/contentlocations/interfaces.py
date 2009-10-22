from zope.interface import Interface

from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations import config
from zope import schema

class IGeoView(Interface):
    """ View to access coordinates """
    def isGeoreferenceable():
        """Returns True if an object is Georeferenceable"""

    def getCoordinates(self):
        """ Public function to get object coordinates """

class IGeoForm(Interface):
    """ Interface for coordinates management forms """

class IGeoManager(Interface):
    """ Interface for shape management """

    coord_type = schema.Choice(
        title=_(u"Type"),
        description=_(u"Choose type of coordinates for uploading csv."),
        vocabulary = 'coordsVocab',
        #values=config.COORDTYPE,
        required=True )

    filecsv = schema.Bytes(
        title=_(u"File"),
        description=_(u"a csv file holding a coordinate per row and enough "
                      u"coordinate pairs for selected type."),
        required=False)

    wkt = schema.Text(
        title=_(u"Coordinates"),
        description=_(u"Shape in WKT format."),
        required=False)

    def isGeoreferenceable(self):
        """ """
    def getCoordinates(self):
        """ """
    def setCoordinates(self):
        """ """
