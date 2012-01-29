from zope.interface import implements, alsoProvides, noLongerProvides
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName

from collective.geo.settings.utils import geo_settings
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.contentlocations.interfaces import IGeoMarker
from collective.geo.contentlocations.interfaces import IGeoMarkerUtility

from collective.geo.contentlocations import ContentLocationsMessageFactory as _


def update_georeferenceable_objects(context, new_ct):
    g_marker = queryUtility(IGeoMarkerUtility)
    if not g_marker:
        return

    ct = getToolByName(context, 'portal_catalog')
    query = {'object_provides':
                'collective.geo.geographer.interfaces.IGeoreferenceable'}
    pt = [item.portal_type for item in ct.searchResults(query)]
    olds_pt = list(set(pt))

    adds = []
    for new in new_ct:
        if new in olds_pt:
            olds_pt.remove(new)
        else:
            adds.append(new)
    if len(olds_pt) == 0 and len(adds) == 0:
        return

    nb_items, bad_items = g_marker.update(context, adds, olds_pt)
    updated = u'%d %s' % (nb_items, _(u'objects updated.'))
    if not bad_items:
        message = updated
    else:
        message = u'%s, %d %s: %s' % (updated,
                                      len(bad_items),
                                      _(u'update(s) on object(s) failed'),
                                      ','.join(bad_items), )
    pu = getToolByName(context, 'plone_utils')
    pu.addPortalMessage(message)


class GeoMarker(object):
    """Utility to mark an object IGeoreferenceable
    """
    implements(IGeoMarker)

    def __init__(self, context):
        """
        """
        self.context = context

    @property
    def _options(self):
        return geo_settings(self.context)

    @property
    def geo_content_types(self):
        """ Return the georeferenceable portal types
        """
        return self._options.geo_content_types

    def process(self):
        """ Proceed to the markage
        """
        try:
            geo_content_types = self.geo_content_types
        except:
            return

        if not self.context.portal_type in geo_content_types:
            self.clear()
        else:
            self.add()

    def add(self):
        """ Add the markage
        """
        if IGeoreferenceable.providedBy(self.context):
            return
        alsoProvides(self.context, IGeoreferenceable)
        self.context.reindexObject(idxs=['object_provides'])

    def clear(self):
        """ Clear the markage
        """
        if not IGeoreferenceable.providedBy(self.context):
            return
        noLongerProvides(self.context, IGeoreferenceable)
        self.context.reindexObject(idxs=['object_provides'])


class GeoMarkerUtility(object):
    implements(IGeoMarkerUtility)

    def update(self, context, news, olds):
        """ Update only objects with a change of configuration
        """
        i = 0
        bad_objects = []
        for new in news:
            j, bads = self._walker(context, 'add', new)
            i += j
            bad_objects += bads
        for old in olds:
            j, bads = self._walker(context, 'clear', old)
            i += j
            bad_objects += bads
        return i, bad_objects

    def updateAll(self, context):
        """ Update all objects on portal
        """
        return self._walker(context, 'process')

    def _walker(self, context, meth, portal_type=''):
        pc = getToolByName(context, 'portal_catalog')
        bad_objects = []
        i = 0
        if portal_type != '':
            brains = pc(portal_type=portal_type)
        else:
            brains = pc()

        for brain in brains:
            try:
                process = getattr(IGeoMarker(brain.getObject()), meth, None)
                if process != None:
                    process()
                i += 1
            except:
                bad_objects.append(brain.getPath())
                continue
        return i, bad_objects
