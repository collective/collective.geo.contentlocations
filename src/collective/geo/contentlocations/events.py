from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from . import utils


class IObjectStylesEvent(IObjectModifiedEvent):
    """An event signaling that an object has been 'geo styled'
    """


class ObjectStylesEvent(object):
    implements(IObjectStylesEvent)

    def __init__(self, ob):
        self.object = ob


def reindexStylesSubscriber(event):
    """A subscriber to IObjectStylesEvent"""
    obj = event.object
    if not utils.isDexterityContentType(obj):
        obj.reindexObject(idxs=['collective_geo_styles'])


def reindexDocSubscriber(event):
    """A subscriber to IObjectGeoreferencedEvent"""
    obj = event.object
    if not utils.isDexterityContentType(obj):
        obj.reindexObject(idxs=['zgeo_geometry'])
