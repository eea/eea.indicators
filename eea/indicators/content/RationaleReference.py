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
from Products.ATContentTypes.content.link import ATLink, ATLinkSchema

##code-section module-header #fill in your manual code here
from Products.CMFPlone.utils import getToolByName
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
        accessor="getDescription",
        searchable=True,
    ),
    StringField(
        name='reference_type',
        widget=SelectionWidget(
            label="Reference type",
            label_msgid='indicators_label_reference_type',
            i18n_domain='indicators',
        ),
        required=True,
        vocabulary=[("RationaleRefType_01", "Scientific reference"), ("RationaleRefType_02", "Reference to other indicator initiative") ],
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RationaleReference_schema = ATLinkSchema.copy() + \
    getattr(ATLink, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RationaleReference(ATLink, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IRationaleReference)

    meta_type = 'RationaleReference'
    _at_rename_after_creation = True

    schema = RationaleReference_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDescription()).getData()



registerType(RationaleReference, PROJECTNAME)
# end of class RationaleReference

##code-section module-footer #fill in your manual code here
##/code-section module-footer



