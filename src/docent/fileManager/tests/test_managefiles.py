# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from docent.fileManager.interfaces import Imanagefiles
from docent.fileManager.testing import DOCENT_FILEMANAGER_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class managefilesIntegrationTest(unittest.TestCase):

    layer = DOCENT_FILEMANAGER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='managefiles')
        schema = fti.lookupSchema()
        self.assertEqual(Imanagefiles, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='managefiles')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='managefiles')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(Imanagefiles.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='managefiles',
            id='managefiles',
        )
        self.assertTrue(Imanagefiles.providedBy(obj))
