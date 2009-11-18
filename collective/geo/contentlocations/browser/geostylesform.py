from zope import interface, component
from zope.app.pagetemplate import viewpagetemplatefile
from zope.event import notify

from z3c.form import field, subform
from z3c.form.interfaces import IEditForm

from collective.z3cform.colorpicker.colorpicker import ColorpickerFieldWidget

from collective.geo.kml.interfaces import IGeoContentKmlForm, IGeoContentKmlSettings
from collective.geo.kml.geokmlconfig import GeoContentKmlSettings

from zgeo.geographer.event import ObjectGeoreferencedEvent

class EditStylesForm(subform.EditSubForm):
    component.adapts(IEditForm)
    interface.implements(IGeoContentKmlForm)

    template = viewpagetemplatefile.ViewPageTemplateFile('subform.pt')

    fields = field.Fields(IGeoContentKmlSettings)

    fields['linecolor'].widgetFactory = ColorpickerFieldWidget
    fields['polygoncolor'].widgetFactory = ColorpickerFieldWidget

    label = u"Custom styles"
    form_name = u"Custom styles"


    def __init__(self, context, request, parent):
       super(EditStylesForm, self).__init__(context, request, parent)
       self.parentForm = parent

       self.contentkmlsettings = GeoContentKmlSettings(self.context)

    def update(self):
        super(EditStylesForm, self).update()

    def processData(self, data):
        self.contentkmlsettings.initialiseStyles(self.context)

        for key, val in data.items():
            if key in field.Fields(IGeoContentKmlSettings).keys():
                self.contentkmlsettings.set(key, val)

        notify(ObjectGeoreferencedEvent(self.context))

    def getContent(self):
        '''See interfaces.IForm'''
        return self.contentkmlsettings.getStyles(self.context)


