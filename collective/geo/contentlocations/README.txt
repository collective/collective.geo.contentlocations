collective.geo.contentlocations Package Readme
==============================

Overview
--------
collective.geo.contentlocations provides graphical interface based on z3c.form for collective.geo.geographer package

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

Georeferenceable objects have another tab (Coordinates), registered in portal_action 
This is the condition to enable them

    >>> document.restrictedTraverse('@@geoview').isGeoreferenceable()
    True
    
Based on the type of geo objects (points, polygons or linestrings) we want different forms

Points:

    >>> import zope.component
    >>> from zope.publisher.browser import TestRequest
    >>> from collective.geo.contentlocations.interfaces import IGeoForm
    >>> zope.component.getMultiAdapter((document, TestRequest()), IGeoForm, 'Point')
    <collective.geo.contentlocations.browser.geoform.GeoPointForm object ...>

LineString:

    >>> zope.component.getMultiAdapter((document, TestRequest()), IGeoForm, 'LineString')
    <collective.geo.contentlocations.browser.geoform.GeoLineStringForm object ...>
    
Polygons:

    >>> zope.component.getMultiAdapter((document, TestRequest()), IGeoForm, 'Polygon')
    <collective.geo.contentlocations.browser.geoform.GeoPolygonForm object ...>

That's all folks

