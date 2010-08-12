import unittest
from collective.geo.contentlocations.tests import base

# from Products.Five.testbrowser import Browser
# from Products.PloneTestCase.setup import portal_owner, default_password
from collective.geo.settings.utils import geo_settings
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.contentlocations.geomarker import update_georeferenceable_objects


class TestGeomanager(base.FunctionalTestCase):

    def afterSetUp(self):
        super(TestGeomanager, self).afterSetUp()
        self.p_types = ('Image', 'Event', 'News Item')

        self.setRoles('Manager')
        def create_obj(context, pt):
            oid = 'test-%s' % pt.lower().replace(' ', '-')
            return context.invokeFactory(pt, oid) 

        self.obj_ids = [create_obj(self.folder, pt) for pt in self.p_types]
        geo_settings(self.portal).geo_content_types

    def test_after_obj_creation(self):
        for oid in self.obj_ids:
            obj = self.folder[oid]
            self.assertFalse(IGeoreferenceable.providedBy(obj))

    def test_add_marker(self):
        new_geo_type = self.p_types[0]
        update_georeferenceable_objects(self.portal, [new_geo_type])
        for oid in self.obj_ids:
            obj = self.folder[oid]
            if obj.portal_type == new_geo_type:
                self.assertTrue(IGeoreferenceable.providedBy(obj))
            else:
                self.assertFalse(IGeoreferenceable.providedBy(obj))

    def test_update_markers(self):
        new_geo_types = self.p_types[1:]
        update_georeferenceable_objects(self.portal, new_geo_types)
        for oid in self.obj_ids:
            obj = self.folder[oid]
            if obj.portal_type in new_geo_types:
                self.assertTrue(IGeoreferenceable.providedBy(obj))
            else:
                self.assertFalse(IGeoreferenceable.providedBy(obj))
                

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGeomanager))
    return suite


# Test Controlopanel
# ==================
# 
# We have extend GeoControlpanelForm defined in collective.geomapwidget to provide a mechanism to
# configure Georeferenceable content types.
# 
# we start the tests with the usual boilerplate
#     >>> from Products.Five.testbrowser import Browser
#     >>> browser = Browser()
#     >>> portal_url = self.portal.absolute_url()
#     >>> self.portal.error_log._ignored_exceptions = ()
# 
# we log in as manager and verify the functionality of collective.geo.mapwidget control panel form;
#     >>> from Products.PloneTestCase.setup import portal_owner
#     >>> browser.addHeader('Authorization',
#     ...                   'Basic %s:%s' % (portal_owner, default_password))
# 
#     >>> browser.open('%s/@@collectivegeo-controlpanel' % portal_url)
# 
#     >>> from collective.geo.geographer.interfaces import IGeoreferenceable
#     >>> from zope.interface import alsoProvides
#     >>> ct = self.portal.portal_catalog
#     >>> query = {'portal_type': 'Document'}
#     >>> brains = ct.searchResults(query)
#     >>> for i in brains:
#     ...     obj = i.getObject()
#     ...     alsoProvides(obj, IGeoreferenceable)
#     ...     obj.reindexObject(idxs=['object_provides'])
# 
# 
# In the extended version of that form we have a new widget
#     >>> widget = browser.getControl(name = 'form.widgets.geo_content_types.to')
# 
#     >>> from collective.geo.settings.utils import geo_settings
#     >>> geo_content_types = geo_settings(self.portal).geo_content_types
#     >>> widget.options == geo_content_types
#     True
# 
#     >>> browser.getControl('Apply').click()
# 
# Check that there weren't any errors
#     >>> 'Data successfully updated.' in browser.contents
#     True