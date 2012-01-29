from zope import interface

from collective.geo.contentlocations.interfaces import IGeoManager

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.geographer.interfaces import IWriteGeoreferenced


class GeoManager(object):
    """We instanciate a GeoManager on a non georeferenceable context
      >>> geo = GeoManager(None)
      >>> geo.isGeoreferenceable()
      False

      coordinates will be None
      >>> geo.getCoordinates()
      (None, None)

      now we create a georeferenceable object
      >>> from zope.annotation.interfaces import IAttributeAnnotatable
      >>> class TestContent(object):
      ...     interface.implements(IGeoreferenceable, IAttributeAnnotatable)
      >>> geofoo = TestContent()
      >>> geo = GeoManager(geofoo)
      >>> geo.isGeoreferenceable()
      True

      we add coordinates to the object (type, (lon, lat))
      >>> geo.setCoordinates('Point', (0.222, 0.111))

      we check the coordinates correctness
      >>> geo.getCoordinates()
      ('Point', (0.222, 0.111))

      being a Point both longitude
      >>> geo.longitude
      0.222

      and latitude
      >>> geo.latitude
      0.111

      have values

      in the same fashion we can set a LineString
      >>> geo.setCoordinates('LineString', ((0.111,0.222),) )

      and get its coordinates
      >>> geo.getCoordinates()
      ('LineString', ((0.111, 0.222),))

      longitude and latitude will be None
      >>> geo.longitude is None
      True

      and latitude
      >>> geo.latitude is None
      True

      We can also change the coordinates to represent a Polygon
      >>> poligon_coords = (((0.111,0.222),(0.222,0.222),
      ...    (0.222,0.111),(0.111,0.111)),)

      >>> geo.setCoordinates('Polygon', poligon_coords)

      and get its coordinates back accordingly
      >>> coords = geo.getCoordinates()
      >>> coords[0]
      'Polygon'
      >>> coords[1] == poligon_coords
      True

      To remove coordinates from an object we can
      call removeCoordinates method

      >>> geo.removeCoordinates()
      >>> geo.getCoordinates()
      (None, None)


    """
    interface.implements(IGeoManager)

    @property
    def coord_type(self):
        return self.getCoordinates()[0]

    @property
    def longitude(self):
        type, coords = self.getCoordinates()
        if type == 'Point':
            return coords[0]
        return None

    @property
    def latitude(self):
        type, coords = self.getCoordinates()
        if type == 'Point':
            return coords[1]
        return None

    @property
    def wkt(self):
        from shapely.geometry.geo import asShape
        try:
            return asShape(IGeoreferenced(self.context).geo).wkt
        except ValueError:
            # context is not a valid shape.
            pass
        return u''

    def __init__(self, context, form=None):
        self.context = context
        self.form = form

    def isGeoreferenceable(self):
        return IGeoreferenceable.providedBy(self.context)

    def getCoordinates(self):
        if(self.isGeoreferenceable()):
            geo = IGeoreferenced(self.context)
            return geo.type, geo.coordinates
        else:
            return None, None

    def setCoordinates(self, type, coords):
        if(self.isGeoreferenceable()):
            geo = IWriteGeoreferenced(self.context)
            geo.setGeoInterface(type, coords)

    def removeCoordinates(self):
        if(self.isGeoreferenceable()):
            geo = IWriteGeoreferenced(self.context)
            geo.removeGeoInterface()
