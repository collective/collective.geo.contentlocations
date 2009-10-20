collective.geo.contentlocations.browser
=======================================

we start the tests with the usual boilerplate
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()

    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url)

We have the login portlet, so let's use that.
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

we have a specific tab for the georeferenceable objects -- Coordinates
    >>> '<a href="%s/front-page/@@manage-coordinates">Coordinates</a>' % portal_url in browser.contents
    True

let's try it!
    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.url == '%s/front-page/@@manage-coordinates' % portal_url
    True

Let's investigate the form a little bit
First check the type list box:
    >>> control = browser.getControl('Type')
    >>> control
    <ListControl name='form.widgets.coord_type:list' type='select'>
    >>> control.options
    ['Point', 'LineString', 'Polygon']

There shouldn't be the GeoPoint Javascript in the page, since we implement our
own WKT-specific widget code
    >>> '<script type="text/javascript" src="++resource++geo-point.js"></script>' not in browser.contents
    True

let's try to submit the form with a new LineString in the wkt-field
    >>> browser.getControl('Coordinates').value = u'LINESTRING '\
    ...           '(153.02719116211 -27.352252938064,'\
    ...           '153.11370849609 -27.370547753645,'\
    ...           '153.08624267578 -27.403470801049,'\
    ...           '153.00933837891 -27.402251603719)'
    >>> browser.getControl('Save').click()

we check that our data is still there
    >>> 'Changes saved.' in browser.contents
    True

    >>> from collective.geo.contentlocations.interfaces import IGeoManager
    >>> geo = IGeoManager(self.portal['front-page'])
    >>> geo.getCoordinates()
    ('LineString', ((153.02719116211, -27.352252938064002), (153.11370849609, -27.370547753644999), (153.08624267578, -27.403470801049), (153.00933837891, -27.402251603719002)))

I might instead click "cancel".
Let's do it again, first clicking on "coordinates" and choosing the
"point" type
    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.getControl('Type')
    <ListControl name='form.widgets.coord_type:list' type='select'>

we're in the coordinates input form
    >>> browser.getControl('Coordinates')
    <Control name='form.widgets.wkt' type='textarea'>

clicking on cancel leads me to the default content view
    >>> browser.getControl('Cancel').click()
    >>> 'No changes made.' in browser.contents
    True

let's choose "polygon"
    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> control = browser.getControl('Type')
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
    >>> browser.getControl('Line color')
    <Control name='styles0.widgets.linecolor' type='text'>
    >>> browser.getControl('Line width')
    <Control name='styles0.widgets.linewidth' type='text'>
    >>> browser.getControl('Polygon color')
    <Control name='styles0.widgets.polygoncolor' type='text'>
    >>> browser.getControl('Marker image size')
    <Control name='styles0.widgets.marker_image_size' type='text'>

    >>> use_custom_styles_control = browser.getControl(name='styles0.widgets.use_custom_style:list')
    >>> use_custom_styles_control
    <ListControl name='styles0.widgets.use_custom_style:list' type='radio'>

We can see the default custom settings on this form

    >>> use_custom_styles_control.value
    ['false']
   
We can set custom settings on this form (per-content)

    >>> use_custom_styles_control.value = ['true']
    >>> browser.getControl('Save').click()

Check to see that saved successfully

    >>> 'Changes saved.' in browser.contents
    True

And check to see if the value was saved onto our content

    >>> document = self.portal['front-page']
    >>> from collective.geo.kml.interfaces import IGeoContentKmlSettings
    >>> kml_settings = IGeoContentKmlSettings(document)
    >>> kml_settings.context = document

    >>> kml_settings.get('use_custom_style')
    True

XXX Everything should work for Point, LineString and Polygon as well
