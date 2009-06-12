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

It is a two steps form:
Firts:
we are asked the type of coordinates to input
    >>> control = browser.getControl('Type')
    >>> control
    <ListControl name='form.widgets.coord_type:list' type='select'>
    >>> control.options
    ['Point', 'LineString', 'Polygon']

set type value and click 'Set' button
    >>> control.value = ['Point',]
    >>> browser.getControl('Set').click()

second:
url is the same; we're still here 
    >>> browser.url == '%s/front-page/@@manage-coordinates' % portal_url
    True

but there is another form 
we set values for latitude and longitude and click save
    >>> browser.getControl('Longitude').value = '0.222'
    >>> browser.getControl('Latitude').value = '0.111'
    >>> browser.getControl('Save').click()

we check that our data is still there
    >>> from collective.geo.contentlocations.interfaces import IGeoManager
    >>> geo = IGeoManager(self.portal['front-page'])
    >>> geo.getCoordinates()
    ('Point', (0.222, 0.111))

I might instead click "cancel".
Let's do it again, first clicking on "coordinates" and choosing a the "point" type
    >>> link = browser.getLink('Coordinates')
    >>> link.click()
    >>> browser.getControl('Type').value = ['Point',]
    >>> browser.getControl('Set').click()

we're in the coordinates input form
    >>> browser.getControl('Latitude')
    <Control name='form.widgets.latitude' type='text'>

clicking on cancel leads me to the first form without saving the data
    >>> browser.getControl('Cancel').click()
    >>> control = browser.getControl('Type')
    >>> control
    <ListControl name='form.widgets.coord_type:list' type='select'>

let's choose "polygon"
    >>> control.value = ['Polygon',]
    >>> browser.getControl('Set').click()

we get a different form
    >>> file_control = browser.getControl('File')
    >>> file_control
    <Control name='form.widgets.filecsv' type='file'>

we load a coordinates csv file and verify saved data
    >>> import cStringIO
    >>> file = cStringIO.StringIO('0.111,0.222\n0.333,0.444')
    >>> file_control.add_file(file,
    ...                       'text/csv', 'coordinates.csv')
    >>> browser.getControl('Save').click()
    >>> geo.getCoordinates()
    ('Polygon', (((0.111, 0.222), (0.33300000000000002, 0.44400000000000001)),))


XXX Everyfing should work for LineString as well
