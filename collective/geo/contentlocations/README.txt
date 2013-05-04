How it Work
-----------

We create a generic Document that implements IGeoreferenceable interface

    >>> import transaction
    >>> portal = layer['portal']
    >>> from plone.app.testing import (TEST_USER_ID, TEST_USER_NAME,
    ...                                TEST_USER_PASSWORD)
    >>> from plone.app.testing import login, setRoles
    >>> setRoles(portal, TEST_USER_ID, ['Manager'])
    >>> login(portal, TEST_USER_NAME)
    >>> oid = portal.invokeFactory('Document', 'base-document')
    >>> document = portal[oid]
    >>> from zope.interface import alsoProvides
    >>> from collective.geo.geographer.interfaces import IGeoreferenceable
    >>> alsoProvides(document, IGeoreferenceable)
    >>> transaction.commit()

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
    >>> transaction.commit()


Try browsing the geo-shape edit view:
-------------------------------------

    >>> from plone.testing.z2 import Browser
    >>> app = layer['app']
    >>> browser = Browser(app)
    >>> portal_url = portal.absolute_url()
    >>> portal.error_log._ignored_exceptions = ()

The edit view is protected so we need to log in

    >>> browser.addHeader('Authorization',
    ...                   'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD))
    >>> browser.open(portal_url)

Create the url and open it

    >>> view_url = '%s/@@manage-coordinates' % document.absolute_url()
    >>> browser.open(view_url)
    >>> '<div id="form-widgets-wkt-map" ' in browser.contents
    True
    >>> 'POINT (0.111' in browser.contents
    True
    >>> ' 0.222' in browser.contents
    True

We should also see the fieldset/fields for custom properties for this content

    >>> 'Custom styles' in browser.contents
    True
