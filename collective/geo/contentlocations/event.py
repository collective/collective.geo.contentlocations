from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

class IObjectStylesEvent(IObjectModifiedEvent):
    """An event signaling that an object has been 'geo styled'
    """

class ObjectStylesEvent(object):
    implements(IObjectStylesEvent)

    def __init__(self, ob):
        self.object = ob


def reindexDocSubscriber(event):
    """A subscriber to ObjectModifiedEvent"""
    event.object.reindexObject()