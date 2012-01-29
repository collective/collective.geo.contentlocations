from persistent.dict import PersistentDict

from zope.interface import implements
from zope.component import getUtility
from zope.event import notify

from zope.annotation.interfaces import IAnnotations

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.settings.interfaces import IGeoFeatureStyle
from collective.geo.contentlocations.events import ObjectStylesEvent
from collective.geo.contentlocations.config import GEO_STYLE_FIELDS


KEY = 'collective.geo.contentlocations.style'


class GeoStyleManager(object):
    """ Adapter to manage features style for content type
    """

    implements(IGeoCustomFeatureStyle)

    def __init__(self, context):

        self.context = context
        self.defaultstyles = getUtility(IRegistry).forInterface(
                                                    IGeoFeatureStyle)

        annotations = IAnnotations(context)
        self.geostyles = annotations.get(KEY, None)
        if not self.geostyles:
            annotations[KEY] = PersistentDict()
            self.geostyles = annotations[KEY]

            #Set our custom styles to be the defaults for all fields
            for field in GEO_STYLE_FIELDS:
                self.geostyles[field] = getattr(
                                self.defaultstyles, field, None)

            #This field isn't present in the defaults so set it manually
            self.geostyles['use_custom_styles'] = False

    def __getattribute__(self, name):
        """Proxy attribute access to our local styles.

        If something has requested one of the fields in our custom styles
        then we get the property from there.  Otherwise, provide access
        normally using the parent method.
        """
        if name in GEO_STYLE_FIELDS:
            return self.get(name)
        else:
            return super(GeoStyleManager, self).__getattribute__(name)

    def set(self, key, val):
        return self.geostyles.__setitem__(key, val)

    def get(self, key, default=False):
        try:
            return self.geostyles.get(key)
        except:
            return default

    def setStyles(self, data):
        changes = False
        for item in data:
            if self.get(item[0]) != item[1]:
                self.set(item[0], item[1])
                changes = True
        if changes:
            notify(ObjectStylesEvent(self.context))
