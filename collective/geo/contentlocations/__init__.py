from zope.i18nmessageid import MessageFactory
import config

ContentLocationsMessageFactory = MessageFactory(config.PROJECTNAME)

_ = ContentLocationsMessageFactory
COORDTYPE = [('Point', _('Point')), 
             ('LineString', _('LineString')), 
             ('Polygon',_('Polygon'))
            ]
