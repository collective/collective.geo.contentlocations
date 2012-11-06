import unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from ..testing import CGEO_CONTENTLOCATIONS_FUNCTIONAL

from collective.geo.settings.utils import geo_settings


class TestControlPanel(unittest.TestCase):

    layer = CGEO_CONTENTLOCATIONS_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.browser = Browser(self.app)

    def test_extended_form(self):
        portal_url = self.portal.absolute_url()

        self.browser.addHeader('Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        self.browser.open('%s/@@collectivegeo-controlpanel' % portal_url)

        widget = None
        try:
            widget = self.browser.getControl(
                    name='form.widgets.geo_content_types.to') or False
        except:
            self.fail(
                'geo_content_types widget not Found in controlpanel form')

        if widget:
            geo_content_types = geo_settings(self.portal).geo_content_types
            self.assertEqual(widget.options, geo_content_types)
