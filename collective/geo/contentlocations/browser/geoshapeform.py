from zope.interface import implements

from z3c.form import form, field, button

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import getToolByName

from plone.z3cform.layout import wrap_form
from plone.z3cform.fieldsets import extensible

from collective.geo.mapwidget.interfaces import IMapView
from collective.geo.mapwidget.browser.widget import MapWidget
from collective.geo.mapwidget.maplayers import MapLayer

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle

from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations.browser.geostylesform \
                                                  import GeoStylesForm
from collective.geo.contentlocations.interfaces import IGeoManager

#from shapely.geos import ReadingError


class GeoShapeForm(extensible.ExtensibleForm, form.Form):
    implements(IMapView)
    template = ViewPageTemplateFile('geoshapeform.pt')
    form_name = "edit_geometry"
    id = 'coordinates-form'
    description = _(u"Specify the geometry for this content")
    fields = field.Fields(IGeoManager).select('wkt')
    mapfields = ['geoshapemap']

    groups = (GeoStylesForm,)

    message_ok = _(u'Changes saved.')
    message_cancel = _(u'No changes made.')
    message_georeference_removed = _(u'Coordinates removed')
    message_coordinates_null = _(u"No coordinate has been set. Please, set "
                                  "coordinates on the map or fill the WKT "
                                  "field.")
    message_error_wkt = _(u'WKT expression not correct. Verify input.')
    message_error_input = _(u'No valid input given.')

    def __init__(self, context, request):
        super(GeoShapeForm, self).__init__(context, request)
        self.geomanager = IGeoManager(self.context)

        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        props_tool = getToolByName(portal, 'portal_properties')
        site_props = getattr(props_tool, 'site_properties')
        self.typesUseViewActionInListings = list(
                    site_props.getProperty('typesUseViewActionInListings'))

    @property
    def next_url(self):
        #Need to send the user to the view url for certain content types.
        url = self.context.absolute_url()
        if self.context.portal_type in self.typesUseViewActionInListings:
            url += '/view'

        return url

    def redirectAction(self):
        self.request.response.redirect(self.next_url)

    def setStatusMessage(self, message, level='info'):
        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(message, level)

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):  # pylint: disable=W0613
        data, errors = self.extractData()
        if (errors):
            return

        # set content geo style
        geostylesgroup = [gr for gr in self.groups \
                    if gr.__class__.__name__ == 'GeoStylesForm']
        if geostylesgroup:
            stylemanager = IGeoCustomFeatureStyle(self.context)
            fields = geostylesgroup[0].fields
            stylemanager.setStyles([(i, data[i]) for i in fields])

        # we remove coordinates if wkt is 'empty'
        message = self.message_ok
        if not data['wkt']:
            geo = IGeoManager(self.context)
            coord = geo.getCoordinates()
            if coord == (None, None):
                self.setStatusMessage(self.message_coordinates_null, 'warning')
            else:
                message = self.message_georeference_removed
                self.geomanager.removeCoordinates()

        else:
            ok, message = self.addCoordinates(data)
            if not ok:
                self.status = message
                return

        self.setStatusMessage(message)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):  # pylint: disable=W0613
        self.setStatusMessage(self.message_cancel)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Remove georeference'), name='remove-georeference')
    def handleRemoveGeoreference(self, action):
        self.geomanager.removeCoordinates()
        self.setStatusMessage(self.message_georeference_removed)
        self.redirectAction()

    def addCoordinates(self, data):
        """ from collective.geo.geographer.README.txt
            Now set the location geometry to type "Point"
            and coordinates 105.08 degrees West,
            40.59 degrees North using setGeoInterface()

            >>> geo.setGeoInterface('Point', (-105.08, 40.59))
        """

        try:
            geom = self.verifyWkt(data['wkt']).__geo_interface__
            self.geomanager.setCoordinates(geom['type'],
                                            geom['coordinates'])
            return True, self.message_ok
        except: #ReadingError: is a subclass of generic exception
            return False, self.message_error_wkt

    def verifyWkt(self, data):
        try:
            from shapely import wkt
            geom = wkt.loads(data)
        except ImportError:
            from pygeoif.geometry import from_wkt
            geom = from_wkt(data)
        return geom


manageCoordinates = wrap_form(GeoShapeForm, label=_(u'Coordinates'),
                  description=_(u"Modify geographical data for this content"))


# class ShapeMapWidget(MapWidget):

#     mapid = 'geoshapemap'
#     _layers = ['shapeedit']

#     @property
#     def js(self):
#         return """
#   jq(window).bind('map-load', function(e, map) {
#     var layer = map.getLayersByName('Edit')[0];
#     var elctl = new OpenLayers.Control.WKTEditingToolbar(layer, {wktid: '%s'});
#     map.addControl(elctl);
#     elctl.activate();
#   });
#         """ % self.view.widgets['wkt'].id


# class ShapeEditLayer(MapLayer):

#     name = 'shapeedit'

#     jsfactory = """
#     function() { return new OpenLayers.Layer.Vector('Edit');}
#     """
