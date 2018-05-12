# -*- coding: utf-8 -*-

import logging
from plone.dexterity.content import Container

from plone.app.contenttypes.content import File
from plone.app.contenttypes.interfaces import IFile

from zope import schema
from zope.interface import Interface

from docent.fileManager import _

logger = logging.getLogger("Plone")


class IManagedFile(IFile):
    """uses dublin core & plone.excludefromnavigation"""


class ManagedFile(File):
    """ducktype of plone.app.ocntenttypes.content.File"""

