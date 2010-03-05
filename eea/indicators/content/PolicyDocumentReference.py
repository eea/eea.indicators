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
from Products.ATContentTypes.content.link import ATLink
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        accessor="Description",
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PolicyDocumentReference_schema = ATContentTypeSchema.copy() + \
    getattr(ATLink, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PolicyDocumentReference(ATCTContent, ATLink, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPolicyDocumentReference)

    meta_type = 'PolicyDocumentReference'
    _at_rename_after_creation = True

    schema = PolicyDocumentReference_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(PolicyDocumentReference, PROJECTNAME)
# end of class PolicyDocumentReference

##code-section module-footer #fill in your manual code here
##/code-section module-footer



