# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime
from plone import api
from plone.api.exc import MissingParameterError
from plone.app.contenttypes.browser.file import FileView
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from plone.app.layout.viewlets.content import ContentHistoryViewlet
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.publisher.browser import TestRequest
from AccessControl.SecurityManagement import newSecurityManager
from plone.protect.utils import addTokenToUrl



class FileManagerView(FileView):

    def __init__(self, context, request):
        super(FileManagerView, self).__init__(context, request)

    def getTableRow(self, version_dict):
        context = self.context
        principal = version_dict.get('principal')
        version_id = version_dict.get('version_id')
        timestamp = version_dict.get('timestamp')
        field_id = version_dict.get('field_id')
        filename = version_dict.get('filename')

        memmber_fullname = 'Unknown'
        if principal:
            try:
                member_data = api.user.get(username=principal)
                if member_data:
                    memmber_fullname = member_data.getProperty('fullname')
            except MissingParameterError:
                memmber_fullname = 'Could Not Locate Member'

        date_str = datetime.fromtimestamp(timestamp).strftime("%A, %B %d, %Y %I:%M:%S")

        download_url = '%s/@@download-version?version_id=%s&field_id=%s&filename=%s' % (context.absolute_url(),
                                                                                        version_id,
                                                                                        field_id,
                                                                                        filename)

        html = "<td>%s</td><td>%s</td><td><a href='%s'>Download</a></td>" % (date_str,
                                                                             memmber_fullname,
                                                                             download_url)

        return html


    def getHistory(self):
        if self.has_manage_history():
            alsoProvides(self.request, IDisableCSRFProtection)

        context = self.context
        portal = api.portal.get()
        repo_tool = api.portal.get_tool(name='portal_repository')
        history_metadata = repo_tool.getHistoryMetadata(self.context)
        max_history = history_metadata.nextVersionId
        retrieved_history = history_metadata.retrieve
        referenced_data_dict = OrderedDict()

        if max_history:
            for i in range(int(max_history)):
                history = retrieved_history(i)
                ref_data = history.get('referenced_data')
                blob_file = None
                for k in ref_data:
                    if k.startswith('CloneNamedFileBlobs'):
                        blob_file = ref_data.get(k)
                meta = history.get('metadata')
                sys_meta = meta.get('sys_metadata')
                if sys_meta:
                    principal = sys_meta.get('principal') or ''
                    timestamp = sys_meta.get('timestamp') or 0
                    parent_dict = sys_meta.get('parent') or {}
                    history_id = parent_dict.get('history_id') or None
                    referenced_data_dict.update({blob_file:{'principal':principal,
                                                            'timestamp':timestamp,
                                                            'history_id':history_id}})

        chv = ContentHistoryViewlet(context, self.request, None, None)
        chv.navigation_root_url = chv.site_url = portal.absolute_url()
        full_history = chv.fullHistory()
        time_lookup_dict = {}
        #import pdb;pdb.set_trace()
        for fh in full_history:
            time_key = fh.get('time') or ''
            version_id = fh.get('version_id')
            time_lookup_dict.update({time_key:version_id})

        versions_dicts = []
        for rd_blob in referenced_data_dict:
            version_id = time_lookup_dict.get(timestamp)
            rd_dict = referenced_data_dict.get(rd_blob)
            timestamp = rd_dict.get('timestamp')
            principal = rd_dict.get('principal')
            file_obj = repo_tool.retrieve(context, version_id).object
            field_id = self.request.get('field_id', IPrimaryFieldInfo(context).fieldname)
            named_file = getattr(file_obj, field_id, None)
            file_name = named_file.filename
            versions_dicts.append({'principal': principal,
                                   'version_id': version_id,
                                   'field_id':field_id,
                                   'filename':file_name,
                                   'timestamp': timestamp})

        dicts_byVersionId = sorted(versions_dicts, key=lambda k: k['version_id'])
        return reversed(dicts_byVersionId)

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