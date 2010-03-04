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

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Description",
    ),
    StringField(
        name='link',
        widget=StringField._properties['widget'](
            label="Link",
            label_msgid='indicators_label_link',
            i18n_domain='indicators',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PolicyDocumentReference_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PolicyDocumentReference(BaseContent, BrowserDefaultMixin):
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



