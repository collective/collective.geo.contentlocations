import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from ..testing import CGEO_CONTENTLOCATIONS_FUNCTIONAL

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.contentlocations.geomarker import \
                                    update_georeferenceable_objects


class TestGeomanager(unittest.TestCase):

    layer = CGEO_CONTENTLOCATIONS_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']

        self.p_types = ('Image', 'Event', 'News Item')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        def create_obj(context, pt):
            oid = 'test-%s' % pt.lower().replace(' ', '-')
            return context.invokeFactory(pt, oid)

        self.obj_ids = [create_obj(self.portal, pt) for pt in self.p_types]

    def test_after_obj_creation(self):
        for oid in self.obj_ids:
            obj = self.portal[oid]
            self.assertFalse(IGeoreferenceable.providedBy(obj))

    def test_add_marker(self):
        new_geo_type = self.p_types[0]
        update_georeferenceable_objects(self.portal, [new_geo_type])
        for oid in self.obj_ids:
            obj = self.portal[oid]
            if obj.portal_type == new_geo_type:
                self.assertTrue(IGeoreferenceable.providedBy(obj))
            else:
                self.assertFalse(IGeoreferenceable.providedBy(obj))

    def test_update_markers(self):
        new_geo_types = self.p_types[1:]
        update_georeferenceable_objects(self.portal, new_geo_types)
        for oid in self.obj_ids:
            obj = self.portal[oid]
            if obj.portal_type in new_geo_types:
                self.assertTrue(IGeoreferenceable.providedBy(obj))
            else:
                self.assertFalse(IGeoreferenceable.providedBy(obj))
