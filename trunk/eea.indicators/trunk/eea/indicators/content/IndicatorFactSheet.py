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
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Title",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        schemata="default",
        searchable=True,
        required=True,
        accessor="Title",
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            label="Description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='assessment',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="More updates on",
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        searchable=True,
    ),
    DateTimeField(
        name='assessment_date',
        widget=DateTimeField._properties['widget'](
            label="Assessment Date",
            label_msgid='indicators_label_assessment_date',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='source_code',
        widget=StringField._properties['widget'](
            label="Source code",
            label_msgid='indicators_label_source_code',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='data_source_providers',
        widget=StringField._properties['widget'](
            label="Data Source Providers",
            label_msgid='indicators_label_data_source_providers',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='EEA_responsible',
        widget=StringField._properties['widget'](
            label="Owner",
            label_msgid='indicators_label_EEA_responsible',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='DEV_responsible',
        widget=StringField._properties['widget'](
            label="ID of manager user",
            label_msgid='indicators_label_DEV_responsible',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='data_source_info',
        widget=TextAreaWidget(
            label="Data source info",
            label_msgid='indicators_label_data_source_info',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='priority_data_flows',
        widget=TextAreaWidget(
            label="Priority data flows",
            label_msgid='indicators_label_priority_data_flows',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='policy_question',
        widget=StringField._properties['widget'](
            label="Policy Question",
            label_msgid='indicators_label_policy_question',
            i18n_domain='indicators',
        ),
        searchable=True,
    ),
    StringField(
        name='dpsir',
        widget=SelectionWidget(
            label="DPSIR",
            label_msgid='indicators_label_dpsir',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        vocabulary=[('D', 'Driving forces'), ('P', 'Pressures'), ('S', 'States'), ('I', 'Impacts'), ('R', 'Reactions')],
        required_for_published=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

IndicatorFactSheet_schema = ATFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
IndicatorFactSheet_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class IndicatorFactSheet(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IIndicatorFactSheet)

    meta_type = 'IndicatorFactSheet'
    _at_rename_after_creation = False

    schema = IndicatorFactSheet_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(IndicatorFactSheet, PROJECTNAME)
# end of class IndicatorFactSheet

##code-section module-footer #fill in your manual code here
##/code-section module-footer



