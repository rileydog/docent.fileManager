# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import docent.fileManager


class DocentFilemanagerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=docent.fileManager)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docent.fileManager:default')


DOCENT_FILEMANAGER_FIXTURE = DocentFilemanagerLayer()


DOCENT_FILEMANAGER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCENT_FILEMANAGER_FIXTURE,),
    name='DocentFilemanagerLayer:IntegrationTesting'
)


DOCENT_FILEMANAGER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCENT_FILEMANAGER_FIXTURE,),
    name='DocentFilemanagerLayer:FunctionalTesting'
)


DOCENT_FILEMANAGER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCENT_FILEMANAGER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='DocentFilemanagerLayer:AcceptanceTesting'
)
