# -*- coding: utf-8 -*-
#
# $Id$
#
# Copyright (c) 2010 by ['Tiberiu Ichim']
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Tiberiu Ichim <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.folder import ATBTreeFolder, ATBTreeFolderSchema

##code-section module-header #fill in your manual code here
from Products.CMFPlone.browser.interfaces import INavigationRoot
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SpecificationsFolder_schema = ATBTreeFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
SpecificationsFolder_schema['related_items'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class SpecificationsFolder(ATBTreeFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISpecificationsFolder)

    meta_type = 'SpecificationsFolder'
    _at_rename_after_creation = True

    schema = SpecificationsFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(SpecificationsFolder, PROJECTNAME)
# end of class SpecificationsFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



