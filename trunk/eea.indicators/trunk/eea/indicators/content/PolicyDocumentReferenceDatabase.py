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

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PolicyDocumentReferenceDatabase_schema = BaseBTreeFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PolicyDocumentReferenceDatabase(BaseBTreeFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPolicyDocumentReferenceDatabase)

    meta_type = 'PolicyDocumentReferenceDatabase'
    _at_rename_after_creation = True

    schema = PolicyDocumentReferenceDatabase_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(PolicyDocumentReferenceDatabase, PROJECTNAME)
# end of class PolicyDocumentReferenceDatabase

##code-section module-footer #fill in your manual code here
##/code-section module-footer



