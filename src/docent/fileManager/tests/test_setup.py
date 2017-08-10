# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from docent.fileManager.testing import DOCENT_FILEMANAGER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that docent.fileManager is properly installed."""

    layer = DOCENT_FILEMANAGER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if docent.fileManager is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'docent.fileManager'))

    def test_browserlayer(self):
        """Test that IDocentFilemanagerLayer is registered."""
        from docent.fileManager.interfaces import (
            IDocentFilemanagerLayer)
        from plone.browserlayer import utils
        self.assertIn(IDocentFilemanagerLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCENT_FILEMANAGER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['docent.fileManager'])

    def test_product_uninstalled(self):
        """Test if docent.fileManager is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'docent.fileManager'))

    def test_browserlayer_removed(self):
        """Test that IDocentFilemanagerLayer is removed."""
        from docent.fileManager.interfaces import \
            IDocentFilemanagerLayer
        from plone.browserlayer import utils
        self.assertNotIn(IDocentFilemanagerLayer, utils.registered_layers())
