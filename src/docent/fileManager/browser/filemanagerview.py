# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.browser.file import FileView
from Acquisition import aq_inner
from zope.component import getMultiAdapter

class FileManagerView(FileView):

    def __init__(self, context, request):
        super(FileManagerView, self).__init__(context, request)

    def get_mimetype_icon(self):
        return super(FileManagerView, self).getMimeTypeIcon(self.context.file)

    def has_manage_history(self):
        current_member = api.user.get_current()
        return api.user.has_permission("Docent.fileManager: manageHistory",
                                       user=current_member,
                                       obj=self.context)

    def versioningEnabled(self):
        context = self.context
        portal_repository = context.portal_repository

        isVersionable = portal_repository.isVersionable(context)

        if portal_repository.supportsPolicy(context, 'at_edit_autoversion') and isVersionable:
            return True

        return False