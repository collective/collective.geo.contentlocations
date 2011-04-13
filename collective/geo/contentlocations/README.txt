How it Work
-----------

We create a generic Document that implements IGeoreferenceable interface

    >>> oid = self.folder.invokeFactory('Document', 'base-document')
    >>> document = self.folder[oid]
    >>> from zope.interface import alsoProvides
    >>> from collective.geo.geographer.interfaces import IGeoreferenceable
    >>> alsoProvides(document, IGeoreferenceable)

The document is georeferenceable with the IGeoManager interface

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


Try browsing the geo-shape edit view:
-------------------------------------

    >>> from Testing.testbrowser import Browser
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
    True
