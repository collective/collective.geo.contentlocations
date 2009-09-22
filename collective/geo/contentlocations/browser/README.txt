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
    >>> geo.getCoordinates()
    (u'Polygon', (((152.78686523438, -27.363230190180001), (152.96264648438, -27.447352944394002), (152.87887573242, -27.522886832325), (152.72506713867, -27.507053374681998), (152.71408081054, -27.430289738862001), (152.78686523438, -27.363230190180001)),))

XXX Everything should work for Point, LineString and Polygon as well
