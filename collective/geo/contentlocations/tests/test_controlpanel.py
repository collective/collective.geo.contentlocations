import unittest
from collective.geo.contentlocations.tests import base

from Testing.testbrowser import Browser
from Products.PloneTestCase.setup import portal_owner, default_password
from collective.geo.settings.utils import geo_settings


class TestControlPanel(base.FunctionalTestCase):

    def afterSetUp(self):
        super(TestControlPanel, self).afterSetUp()
        self.browser = Browser()

    def test_extended_form(self):
        portal_url = self.portal.absolute_url()

        self.browser.addHeader('Authorization',
                'Basic %s:%s' % (portal_owner, default_password))
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


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestControlPanel))
    return suite
