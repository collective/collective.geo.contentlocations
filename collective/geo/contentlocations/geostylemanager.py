from persistent.dict import PersistentDict

from zope.interface import implements
from zope.component import getUtility
from zope.event import notify

from zope.annotation.interfaces import IAnnotations

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from collective.geo.contentlocations.events import ObjectStylesEvent

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
            self.geostyles['use_custom_styles'] = False
            self.geostyles['linecolor'] = self.defaultstyles.linecolor
            self.geostyles['linewidth'] = self.defaultstyles.linewidth
            self.geostyles['polygoncolor'] = self.defaultstyles.polygoncolor
            self.geostyles['marker_image'] = self.defaultstyles.marker_image
            self.geostyles['marker_image_size'] = self.defaultstyles.marker_image_size
            self.geostyles['display_properties'] = self.defaultstyles.display_properties
            self.geostyles['map_display_manager'] = self.defaultstyles.map_display_manager

    @property
    def use_custom_styles(self):
        return self.get('use_custom_styles')

    @property
    def linecolor(self):
        return self.get('linecolor')

    @property
    def linewidth(self):
        return self.get('linewidth')

    @property
    def polygoncolor(self):
        return self.get('polygoncolor')

    @property
    def marker_image(self):
        return self.get('marker_image')

    @property
    def marker_image_size(self):
        return self.get('marker_image_size')

    @property
    def display_properties(self):
        return self.get('display_properties')

    @property
    def map_display_manager(self):
        return self.get('map_display_manager')

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
