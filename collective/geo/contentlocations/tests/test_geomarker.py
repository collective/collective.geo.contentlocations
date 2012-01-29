import unittest
from collective.geo.contentlocations.tests import base

# from collective.geo.settings.utils import geo_settings
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.contentlocations.geomarker import \
                                    update_georeferenceable_objects


class TestGeomanager(base.FunctionalTestCase):

    def afterSetUp(self):
        super(TestGeomanager, self).afterSetUp()
        self.p_types = ('Image', 'Event', 'News Item')

        self.setRoles('Manager')

        def create_obj(context, pt):
            oid = 'test-%s' % pt.lower().replace(' ', '-')
            return context.invokeFactory(pt, oid)

        self.obj_ids = [create_obj(self.folder, pt) for pt in self.p_types]
        # geo_settings(self.portal).geo_content_types

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
