from zope.interface import implements
from zope.interface.interfaces import IInterface
from zope.component import queryAdapter, queryUtility
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from collective.geo.contentlocations.interfaces import IGeoMarker
from collective.geo.contentlocations.geomarker import update_georeferenceable_objects


def is_contentlocations_installed():
    i_name = u'collective.geo.contentlocations.interfaces.IGeoMarkerUtility'
    return queryUtility(IInterface, name=i_name, default=False)


class IObjectStylesEvent(IObjectModifiedEvent):
    """An event signaling that an object has been 'geo styled'
    """


class ObjectStylesEvent(object):
    implements(IObjectStylesEvent)

    def __init__(self, ob):
        self.object = ob


def reindexDocSubscriber(event):
    """A subscriber to ObjectModifiedEvent"""
    event.object.reindexObject(idxs=['collective_geo_styles'])


def updateGeoObjects(event):
    if not is_contentlocations_installed():
        return
    update_georeferenceable_objects(event.context,
                    event.data.get('geo_content_types', []))


def markGeoObject(obj, event):
    """Mark an object Georeferenceable"""
    if not queryAdapter(obj, IGeoMarker) or \
            not is_contentlocations_installed():
        return
    try:
        IGeoMarker(obj).process()
    except AttributeError, e:
        print "collective.geo.contentlocations markObject: error in event"
        return
