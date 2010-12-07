from z3c.form import field
from plone.z3cform.fieldsets import group

# from collective.z3cform.colorpicker.colorpicker import ColorpickerFieldWidget
from collective.z3cform.colorpicker.colorpickeralpha import ColorpickerAlphaFieldWidget

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.contentlocations import ContentLocationsMessageFactory as _


class GeoStylesForm(group.Group):
    fields = field.Fields(IGeoCustomFeatureStyle).select('use_custom_styles',
                                                         'linecolor',
                                                         'linewidth',
                                                         'polygoncolor',
                                                         'marker_image',
                                                         'marker_image_size',
                                                         'display_properties',
                                                         'map_display_manager')

    fields['linecolor'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['polygoncolor'].widgetFactory = ColorpickerAlphaFieldWidget

    label = _(u"Custom styles")
