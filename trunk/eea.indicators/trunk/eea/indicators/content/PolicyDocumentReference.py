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
from Products.CMFPlone.utils import getToolByName
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
        validators=('unique_policy_title_validator',),
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),
    StringField(
        name='remoteUrl',
        widget=StringField._properties['widget'](
            label='Remoteurl',
            label_msgid='indicators_label_remoteUrl',
            i18n_domain='indicators',
        ),
        searchable=True,
        validators=('isURL', 'unique_policy_url_validator'),
        default="http://",
        required=True,
        primary=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PolicyDocumentReference_schema = ATContentTypeSchema.copy() + \
    getattr(ATLink, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
finalizeATCTSchema(PolicyDocumentReference_schema)
PolicyDocumentReference_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
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

    # Manually created methods

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDescription()).getData()



registerType(PolicyDocumentReference, PROJECTNAME)
# end of class PolicyDocumentReference

##code-section module-footer #fill in your manual code here
##/code-section module-footer



