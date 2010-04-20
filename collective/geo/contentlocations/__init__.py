from zope.i18nmessageid import MessageFactory
import config

ContentLocationsMessageFactory = MessageFactory(config.PROJECTNAME)

_ = ContentLocationsMessageFactory
COORDTYPE = [('Point', _(u'Point')),
             ('LineString', _(u'LineString')),
             ('Polygon', _(u'Polygon'))]
