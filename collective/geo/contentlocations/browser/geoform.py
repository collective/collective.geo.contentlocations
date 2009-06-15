import csv, cStringIO
from zope import interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.app.pagetemplate import viewpagetemplatefile

from Products.CMFPlone.utils import getToolByName

from plone.z3cform import z2
from z3c.form import form, field, button
from z3c.form.interfaces import HIDDEN_MODE

from zope.component import getMultiAdapter

from collective.geo.geopoint.geopointform import GeopointBaseForm
from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.contentlocations.interfaces import IGeoForm


class manageCoordinates(BrowserView):
    __call__ = ViewPageTemplateFile('geoform.pt')

    label = _(u'Coordinates')
    description = _(u"Modify geographical data for this content")

    def contents(self):
        z2.switch_on(self)
        coord_type = self.request.form.get('form.widgets.coord_type',['',])[0]

        form = getMultiAdapter((self.context,self.request), IGeoForm, coord_type)
        form.update()
        return form.render()


class GeoTypeForm(form.Form):
    interface.implements(IGeoForm)


    fields = field.Fields(IGeoManager).select('coord_type')

    def __init__(self, context, request):
        super(GeoTypeForm,self).__init__(context,request)

    @button.buttonAndHandler(_(u'Next'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if (errors or data['coord_type'] == None):
            return


class BaseForm(form.Form):
    interface.implements(IGeoForm)
    message_ok = _(u'Changes saved.')
    message_cancel = _(u'No changes made.')
    message_error_csv = _(u'CSV File not correct. Verify file format.')

    def __init__(self, context,  request):
        super(BaseForm,  self).__init__(context,  request)
        self.geomanager = IGeoManager(self.context)

    def updateWidgets(self):
        super(BaseForm,self).updateWidgets()
        self.widgets['coord_type'].mode = HIDDEN_MODE
        self.widgets['coord_type'].update()

    @property
    def next_url(self):
        return '%s/@@manage-coordinates' % self.context.absolute_url()

    def redirectAction(self):
        self.request.response.redirect(self.next_url)

    def setStatusMessage(self, message):
        ptool = getToolByName(self.context,'plone_utils')
        ptool.addPortalMessage(message)

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()

        if (errors):
            return

        if not self.addCoordinates(data):
            self.status = self.message_error_csv
            return

        self.setStatusMessage(self.message_ok)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self.setStatusMessage(self.message_cancel)
        self.redirectAction()

    def addCoordinates(self, data):
        raise NotImplementedError


class GeoPointForm(GeopointBaseForm, BaseForm):
    template = viewpagetemplatefile.ViewPageTemplateFile('geopointform.pt')
    fields = field.Fields(IGeoManager).select('coord_type', 'latitude', 'longitude')

    def addCoordinates(self, data):
        """ from zgeo.geographer.README.txt
            Now set the location geometry to type "Point" and coordinates 105.08 degrees
            West, 40.59 degrees North using setGeoInterface()

            >>> geo.setGeoInterface('Point', (-105.08, 40.59))
        """

        self.geomanager.setCoordinates('Point', (data['longitude'], data['latitude']))
        return True


class GeoMultiPointForm(BaseForm):
    fields = field.Fields(IGeoManager).select('coord_type', 'filecsv')
    ignoreContext=True

    def verifyCsv(self,filecsv):
        reader = csv.reader(cStringIO.StringIO(filecsv), delimiter=',')
        coords = []
        for row in reader:
            # check for row existence ???
            # are there any problems if the row is empty ???
            if row:
                # verify pairs of values are there
                try:
                    latitude = row[0]
                    longitude = row[1]
                except:
                    return False

                # verify that latitude and longitude are non-empty and non-zero
                if latitude != '' and longitude != '':
                    try:
                        # check for float convertible values
                        coords.append((float(latitude),float(longitude)))
                    except:
                        return False

        return coords

    def csv2coordinates(self,filecsv):
        csv_data = self.verifyCsv(filecsv)
        if csv_data != False:
            return tuple(csv_data)
        return False


class GeoLineStringForm(GeoMultiPointForm):
    def addCoordinates(self, data):
        coords = self.csv2coordinates(data['filecsv'])
        if coords:
            self.geomanager.setCoordinates('LineString', coords)
            return True

        return False


class GeoPolygonForm(GeoMultiPointForm):
    def addCoordinates(self, data):
        coords = self.csv2coordinates(data['filecsv'])
        if coords:
            self.geomanager.setCoordinates('Polygon', (coords,) )
            return True

        return False
