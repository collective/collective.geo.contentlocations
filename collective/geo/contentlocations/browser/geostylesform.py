from z3c.form import field
from plone.z3cform.fieldsets import group

from collective.z3cform.colorpicker.colorpickeralpha import \
                                        ColorpickerAlphaFieldWidget

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations.config import GEO_STYLE_FIELDS


class GeoStylesForm(group.Group):
    fields = field.Fields(IGeoCustomFeatureStyle).select(*GEO_STYLE_FIELDS)

    fields['linecolor'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['polygoncolor'].widgetFactory = ColorpickerAlphaFieldWidget

    label = _(u"Custom styles")
