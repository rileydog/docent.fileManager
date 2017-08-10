# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from plone import api

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'docent.fileManager:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    file_type = portal.portal_types.get('File', None)
    if file_type:
        updated_view_methods = ['view_history']
        for i in file_type.view_methods:
            updated_view_methods.append(i)
        file_type.view_methods = tuple(set(updated_view_methods))

        file_type.default_view = 'view_history'





def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    portal = api.portal.get()
    file_type = portal.portal_types.get('File', None)
    if file_type:
        updated_view_methods = []
        for i in file_type.view_methods:
            if i == 'view_history':
                continue
            updated_view_methods.append(i)

        file_type.view_methods = tuple(set(updated_view_methods))
        if 'file_view' in file_type.view_methods:
            file_type.default_view = 'file_view'
        else:
            file_type.default_view = file_type.view_methods[0]