Coordinates form
----------------

We start the tests with the usual boilerplate and we log in as manager

    >>> import transaction
    >>> from plone.testing.z2 import Browser
    >>> app = layer['app']
    >>> browser = Browser(app)
    >>> portal = layer['portal']
    >>> from plone.app.testing import (TEST_USER_ID, TEST_USER_NAME,
    ...                                TEST_USER_PASSWORD)
    >>> from plone.app.testing import login, setRoles
    >>> setRoles(portal, TEST_USER_ID, ['Manager'])
    >>> login(portal, TEST_USER_NAME)
    >>> portal_url = portal.absolute_url()
    >>> portal.error_log._ignored_exceptions = ()
    >>> browser.addHeader('Authorization',
    ...                   'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD))

Now we create a document in user folder and we mark it as Georeferenceable

    >>> document_id = portal.invokeFactory('Document', 'document')
    >>> document = portal[document_id]
    >>> transaction.commit()

we don't have a coordinates in the edit bar until we haven't chosen a content as georeferenceable in collective.geo control panel.

    >>> document_url = document.absolute_url()
    >>> browser.open(document_url)
    >>> '<a href="%s/@@manage-coordinates">Coordinates</a>' % document_url in browser.contents
    False

we set Document as geo referenceable content type
    >>> from collective.geo.settings.utils import geo_settings
    >>> geo_settings().geo_content_types = ['Document']
    >>> transaction.commit()

and now we have a link *Coordinates* in  the edit bar

    >>> browser.open(document_url)
    >>> '<a href="%s/@@manage-coordinates">Coordinates</a>' % document_url in browser.contents
    True

let's try it!

    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.url == '%s/@@manage-coordinates' % document_url
    True

Let's try to submit the form with a new LineString in the WKT-field

    >>> browser.getControl(name='form.widgets.wkt').value = u'LINESTRING '\
    ...           '(153.02719116211 -27.352252938064,'\
    ...           '153.11370849609 -27.370547753645,'\
    ...           '153.08624267578 -27.403470801049,'\
    ...           '153.00933837891 -27.402251603719)'
    >>> browser.getControl('Save').click()


we check that our data is still there

    >>> 'Changes saved.' in browser.contents
    True
    >>> from collective.geo.contentlocations.interfaces import IGeoManager
    >>> geo = IGeoManager(document)
    >>> geo.getCoordinates()[0]
    'LineString'
    >>> [(round(c[0],4), round(c[1],4)) for c in geo.getCoordinates()[1]]
    [(153.0272, -27.3523), (153.1137, -27.3705), (153.0862, -27.4035), (153.0093, -27.4023)]

We can remove coordinates from an object using Remove georeference button
    >>> browser.getLink('Coordinates').click()
    >>> browser.getControl('Remove georeference').click()
    >>> 'Coordinates removed' in browser.contents
    True

geo manager adapter will return null coordiantes
    >>> geo.getCoordinates()
    (None, None)

We can also remove the coordinates by deleting data from Wkt textarea
    >>> geo.setCoordinates('Point', (0.111, 0.222))
    >>> transaction.commit()
    >>> browser.getLink('Coordinates').click()
    >>> browser.getControl(name='form.widgets.wkt').value = u''
    >>> browser.getControl('Save').click()
    >>> 'Coordinates removed' in browser.contents
    True

and geo manager adapter returns null coordiantes
    >>> geo.getCoordinates()
    (None, None)

without coordinates we have a warning
    >>> browser.getLink('Coordinates').click()
    >>> browser.getControl('Save').click()
    >>> 'No coordinate has been set.' in browser.contents
    True
    >>> 'Changes saved.' in browser.contents
    True


I might instead click "cancel".
Let's do it again, first clicking on "coordinates"

    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.getControl(name='form.widgets.wkt')
    <Control name='form.widgets.wkt' type='textarea'>

clicking on cancel leads me to the default content view

    >>> browser.getControl('Cancel').click()
    >>> 'No changes made.' in browser.contents
    True

Set map's custom style
----------------------

We can also set a few custom properties on a per-content basis as well
    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.getControl(name='form.widgets.wkt').value = u'POINT (0.111 0.222)'


Check to see if our custom style section is present, with our fields

    >>> 'Custom styles' in browser.contents
    True
    >>> browser.getControl('Use custom styles?')
    <ItemControl name='form.widgets.use_custom_styles:list' type='checkbox' optionValue='selected' selected=False>
    >>> browser.getControl('Map width')
    <Control name='form.widgets.map_width' type='text'>
    >>> browser.getControl('Map height')
    <Control name='form.widgets.map_height' type='text'>
    >>> browser.getControl('Map position')
    <ListControl name='form.widgets.map_viewlet_position:list' type='select'>
    >>> browser.getControl('Line color')
    <Control name='form.widgets.linecolor' type='text'>
    >>> browser.getControl('Line width')
    <Control name='form.widgets.linewidth' type='text'>
    >>> browser.getControl('Polygon color')
    <Control name='form.widgets.polygoncolor' type='text'>
    >>> browser.getControl('Marker image size')
    <Control name='form.widgets.marker_image_size' type='text'>

We can set custom settings on this form (per-content)

    >>> browser.getControl('Use custom styles?').click()
    >>> browser.getControl('Map width').value = "123px"
    >>> browser.getControl('Map height').value = "50%"
    >>> browser.getControl('Line width').value = "2.1"
    >>> browser.getControl('Save').click()

Check to see that saved successfully

    >>> 'Changes saved.' in browser.contents
    True
    >>> from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
    >>> style_config = IGeoCustomFeatureStyle(document)
    >>> style_config.use_custom_styles
    True
    >>> style_config.map_width
    u'123px'
    >>> style_config.map_height
    u'50%'
    >>> style_config.linewidth == 2.1
    True
