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
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Question",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
        searchable=True,
    ),
    BooleanField(
        name='is_key_question',
        widget=BooleanField._properties['widget'](
            label="Is this a key question?",
            label_msgid='indicators_label_is_key_question',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            visible={'view':'invisible', 'edit':'invisible'},
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        accessor="Description",
        searchable=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PolicyQuestion_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PolicyQuestion(ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPolicyQuestion)

    meta_type = 'PolicyQuestion'
    _at_rename_after_creation = False

    schema = PolicyQuestion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(PolicyQuestion, PROJECTNAME)
# end of class PolicyQuestion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



