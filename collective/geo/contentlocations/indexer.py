from zope.component.interfaces import ComponentLookupError
from collective.geo.settings.interfaces import IGeoFeatureStyle
from plone.indexer.decorator import indexer
from zope import interface


@indexer(interface.Interface)
def collective_geo_styles(object):
    try:
        return IGeoFeatureStyle(object).geostyles
    except (ComponentLookupError, TypeError, ValueError, KeyError, IndexError):
        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError
