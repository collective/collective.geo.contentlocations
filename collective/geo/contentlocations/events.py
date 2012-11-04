from zope.interface import implements
from zope.component import queryAdapter

from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from collective.geo.contentlocations.interfaces import IGeoMarker
from collective.geo.contentlocations.geomarker import \
                                  update_georeferenceable_objects


class IObjectStylesEvent(IObjectModifiedEvent):
    """An event signaling that an object has been 'geo styled'
    """


class ObjectStylesEvent(object):
    implements(IObjectStylesEvent)

    def __init__(self, ob):
        self.object = ob


def reindexStylesSubscriber(event):
    """A subscriber to ObjectModifiedEvent"""
    event.object.reindexObject(idxs=['collective_geo_styles'])


def reindexDocSubscriber(event):
    """A subscriber to ObjectModifiedEvent"""
    event.object.reindexObject(idxs=['zgeo_geometry'])


def updateGeoObjects(event):
    update_georeferenceable_objects(event.context,
                    event.data.get('geo_content_types', []))


def markGeoObject(obj, event):  # pylint: disable=W0613
    """Mark an object Georeferenceable"""
    if not queryAdapter(obj, IGeoMarker):
        return
    try:
        IGeoMarker(obj).process()
    except AttributeError:
        print "collective.geo.contentlocations markObject: error in event"
        return
