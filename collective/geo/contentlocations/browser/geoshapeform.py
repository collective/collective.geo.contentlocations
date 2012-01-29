import csv
import cStringIO
from zope.interface import implements

from zope.app.pagetemplate import viewpagetemplatefile

from Products.CMFPlone.utils import getToolByName

from plone.z3cform.layout import wrap_form
from z3c.form import form, field, button
from plone.z3cform.fieldsets import extensible, group

from collective.geo.mapwidget.interfaces import IMapView
from collective.geo.mapwidget.browser.widget import MapWidget
from collective.geo.mapwidget.maplayers import MapLayer

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle

from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations.browser.geostylesform \
                                                  import GeoStylesForm
from collective.geo.contentlocations.interfaces import IGeoManager

from shapely.geos import ReadingError


class CsvGroup(group.Group):
    fields = field.Fields(IGeoManager).select('coord_type', 'filecsv')
    label = _(u"CSV Import")
    description = _(u"Import data from CSV file")


class GeoShapeForm(extensible.ExtensibleForm, form.Form):
    implements(IMapView)
    template = viewpagetemplatefile.ViewPageTemplateFile('geoshapeform.pt')
    form_name = "edit_geometry"
    description = _(u"Specify the geometry for this content")
    fields = field.Fields(IGeoManager).select('wkt')
    mapfields = ['geoshapemap']

    groups = (CsvGroup, GeoStylesForm)

    message_ok = _(u'Changes saved.')
    message_cancel = _(u'No changes made.')
    message_coordaintes_removed = _(u'Coordinates removed')
    message_coordinates_null = _(u"No coordinate has been set. Please, set "
                                  "coordinates on the map, fill in the WKT "
                                  "field or import a CSV file.")
    message_error_csv = _(u'CSV File not correct. Verify file format.')
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

    def setStatusMessage(self, message):
        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(message)

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

        csv_group = [gr for gr in self.groups \
                    if gr.__class__.__name__ == 'CsvGroup']
        filecsv = csv_group[0].widgets['filecsv'].value

        # we remove coordinates if wkt and filecsv are 'empty'
        message = self.message_ok
        if not data['wkt'] and not filecsv:
            message = self.message_coordaintes_removed
            self.geomanager.removeCoordinates()
        else:
            ok, message = self.addCoordinates(data, filecsv)
            if not ok:
                self.status = message
                return

        self.setStatusMessage(message)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):  # pylint: disable=W0613
        self.setStatusMessage(self.message_cancel)
        self.redirectAction()

    def addCoordinates(self, data, filecsv):
        """ from collective.geo.geographer.README.txt
            Now set the location geometry to type "Point"
            and coordinates 105.08 degrees West,
            40.59 degrees North using setGeoInterface()

            >>> geo.setGeoInterface('Point', (-105.08, 40.59))
        """
        if filecsv:
            filecsv.seek(0)
            coords = self.csv2coordinates(filecsv.read())
            if coords:
                # should probably use dataconvert instead of array indexing
                shape = self.groups[0].widgets['coord_type'].value[0]
                if shape.lower() == 'polygon':
                    # Polygon expects an outer hull and a hole.
                    coords = (coords, )
                self.geomanager.setCoordinates(shape, coords)
                return True, self.message_ok
            else:
                return False, self.message_error_csv
        else:
            try:
                geom = self.verifyWkt(data['wkt']).__geo_interface__
                self.geomanager.setCoordinates(geom['type'],
                                                geom['coordinates'])
                return True, self.message_ok
            except ReadingError:
                return False, self.message_error_wkt
        return False, self.message_error_input

    #Verify the incoming CSV file and read coordinates as per the
    #WGS 1984 reference system (longitude, latitude)
    def verifyCsv(self, filecsv):
        reader = csv.reader(cStringIO.StringIO(str(filecsv)), delimiter=',')
        coords = []
        for row in reader:
            # check for row existence ???
            # are there any problems if the row is empty ???
            if row:
                # verify pairs of values are there
                try:
                    longitude = row[0]
                    latitude = row[1]
                except:
                    return False

                # verify that longitude and latitude are non-empty and non-zero
                if longitude != '' and latitude != '':
                    try:
                        # check for float convertible values
                        coords.append((float(longitude), float(latitude)))
                    except:
                        return False

        return coords

    def csv2coordinates(self, csv_data):
        csv_data = self.verifyCsv(csv_data)
        if csv_data != False:
            return tuple(csv_data)
        return False

    def verifyWkt(self, data):
        from shapely import wkt
        geom = wkt.loads(data)
        return geom


manageCoordinates = wrap_form(GeoShapeForm, label=_(u'Coordinates'),
                  description=_(u"Modify geographical data for this content"))


class ShapeMapWidget(MapWidget):

    mapid = 'geoshapemap'
    _layers = ['shapeedit']

    @property
    def js(self):
        return """
  jq(window).bind('load', function() {
    var map = cgmap.config['geoshapemap'].map;
    var layer = map.getLayersByName('Edit')[0];
    var elctl = new OpenLayers.Control.WKTEditingToolbar(layer, {wktid: '%s'});
    map.addControl(elctl);
    elctl.activate();
  });
        """ % self.view.widgets['wkt'].id


class ShapeEditLayer(MapLayer):

    name = 'shapeedit'

    jsfactory = """
    function() { return new OpenLayers.Layer.Vector('Edit');}
    """
