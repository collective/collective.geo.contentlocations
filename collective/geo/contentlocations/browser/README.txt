Coordinates form
----------------

We start the tests with the usual boilerplate and we log in as manager

    >>> browser = self.browser
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner
    >>> from Products.PloneTestCase.setup import default_password
    >>> browser.addHeader('Authorization',
    ...                   'Basic %s:%s' % (portal_owner, default_password))

Now we create a document in user folder and we mark it as Georeferenceable

    >>> document_id = self.folder.invokeFactory('Document', 'document')
    >>> document = self.folder[document_id]
    >>> from zope.interface import alsoProvides
    >>> from collective.geo.geographer.interfaces import IGeoreferenceable
    >>> alsoProvides(document, IGeoreferenceable)

We have a specific tab for the georeferenceable objects -- Coordinates

    >>> document_url = document.absolute_url()
    >>> browser.open(document_url)
    >>> '<a href="%s/@@manage-coordinates">Coordinates</a>' % document_url in browser.contents
    True

let's try it!

    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.url == '%s/@@manage-coordinates' % document_url
    True

Let's investigate the form a little bit
First check the type list box:

    >>> control = browser.getControl('Type', index=0)
    >>> control
    <ListControl name='form.widgets.coord_type:list' type='select'>
    >>> control.options
    ['Point', 'LineString', 'Polygon']

There shouldn't be the GeoPoint Javascript in the page, since we implement our
own WKT-specific widget code

    >>> '<script type="text/javascript" src="++resource++geo-point.js"></script>' not in browser.contents
    True

let's try to submit the form with a new LineString in the WKT-field

    >>> browser.getControl('Shape in WKT format').value = u'LINESTRING '\
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
    >>> geo.getCoordinates()
    ('LineString', ((153.02719116211, -27.352252938064002), (153.11370849609, -27.370547753644999), (153.08624267578, -27.403470801049), (153.00933837891, -27.402251603719002)))


We can remove coordinates from an object by removing data from Wkt textarea
    >>> browser.getLink('Coordinates').click()
    >>> browser.getControl('Shape in WKT format').value = u''
    >>> browser.getControl('Save').click()
    >>> 'Coordinates removed' in browser.contents
    True

geo manager adapter will return null coordiantes
    >>> geo = IGeoManager(document)
    >>> geo.getCoordinates()
    (None, None)

I might instead click "cancel".
Let's do it again, first clicking on "coordinates" and choosing the "point" type

    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.getControl('Type', index=0)
    <ListControl name='form.widgets.coord_type:list' type='select'>

we're in the coordinates input form

    >>> browser.getControl('Shape in WKT format')
    <Control name='form.widgets.wkt' type='textarea'>

clicking on cancel leads me to the default content view

    >>> browser.getControl('Cancel').click()
    >>> 'No changes made.' in browser.contents
    True

let's choose "polygon"

    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> control = browser.getControl('Type', index=0)
    >>> control.value = ['Polygon',]
    >>> file_control = browser.getControl('File')
    >>> file_control
    <Control name='form.widgets.filecsv' type='file'>

we load a coordinates csv file and verify saved data

    >>> csvdata = '152.78686523438, -27.36323019018\n'\
    ...           '152.96264648438, -27.447352944394\n'\
    ...           '152.87887573242, -27.522886832325\n'\
    ...           '152.72506713867, -27.507053374682\n'\
    ...           '152.71408081054, -27.430289738862\n'\
    ...           '152.78686523438, -27.36323019018'
    >>> import cStringIO
    >>> csvfile = cStringIO.StringIO(csvdata)
    >>> file_control.add_file(csvfile, 'text/csv', 'poly.csv')
    >>> browser.getControl('Save').click()

Check there wasn't an error message

    >>> 'CSV File not correct. Verify file format.' in browser.contents
    False
    >>> 'Changes saved.' in browser.contents
    True
    >>> geo.getCoordinates()
    (u'Polygon', (((152.78686523438, -27.363230190180001), (152.96264648438, -27.447352944394002), (152.87887573242, -27.522886832325), (152.72506713867, -27.507053374681998), (152.71408081054, -27.430289738862001), (152.78686523438, -27.363230190180001)),))

We can also set a few custom properties on a per-content basis as well

    >>> link = browser.getLink('Coordinates')
    >>> link.click()

Check to see if our custom style section is present, with our fields

    >>> 'Custom styles' in browser.contents
    True
    >>> browser.getControl('Use custom styles?')
    <ItemControl name='form.widgets.use_custom_styles:list' type='checkbox' optionValue='selected' selected=False>
    >>> browser.getControl('Map width')
    <Control name='form.widgets.map_width' type='text'>
    >>> browser.getControl('Map height')
    <Control name='form.widgets.map_height' type='text'>
    >>> browser.getControl('Map display position')
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
