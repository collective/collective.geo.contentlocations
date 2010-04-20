collective.geo.contentlocations Package Readme
==============================================

Overview
--------

collective.geo.contentlocations provides graphical interface based on
z3c.form for collective.geo.geographer package

Tests
-----

We create a generic Document

    >>> self.folder.invokeFactory('Document', 'base-document')
    'base-document'

The document is georeferenceable with the IGeoManager interface

    >>> document = self.folder['base-document']
    >>> from collective.geo.contentlocations.interfaces import IGeoManager
    >>> geo = IGeoManager(document)
    >>> geo.isGeoreferenceable()
    True

The coordinates at this moment are unset

    >>> geo.getCoordinates()
    (None, None)

we set the coordinates and verify

    >>> geo.setCoordinates('Point', (0.111, 0.222))
    >>> geo.getCoordinates()
    ('Point', (0.111, 0.222))

Georeferenceable objects have another tab (Coordinates), registered in
portal_action This is the condition to enable them

    >>> document.restrictedTraverse('@@geoview').isGeoreferenceable()
    True

Try browsing the geo-shape edit view:
-------------------------------------

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()

The edit view is protected so we need to log in
    >>> from Products.PloneTestCase.setup import (portal_owner,
    ...                                          default_password)
    >>> browser.addHeader('Authorization',
    ...                   'Basic %s:%s' % (portal_owner, default_password))
    >>> browser.open(portal_url)

Create the url and open it

    >>> view_url = '%s/@@manage-coordinates' % document.absolute_url()
    >>> browser.open(view_url)
    >>> '<div id="geoshapemap" ' in browser.contents
    True
    >>> 'POINT (0.1110000000000000 0.2220000000000000)' in browser.contents
    True

We should also see the fieldset/fields for custom properties for this content
    >>> 'Custom styles' in browser.contents
    False
    >>> 'Use custom styles' in browser.contents
    False

That's all folks
