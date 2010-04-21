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

import interfaces
from zope.interface import implements
from Products.Archetypes.atapi import *
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.OrderableReferenceField._field import OrderableReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

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
        vocabulary=[('None', ''), ('D', 'Driving forces'), ('P', 'Pressures'), ('S', 'States'), ('I', 'Impacts'), ('R', 'Reactions')],
    ),
    OrderableReferenceField(
        'relatedItems',
        relationship = 'relatesTo',
        multiValued = True,
        isMetadata = True,
        languageIndependent = False,
        index = 'KeywordIndex',
        write_permission = ModifyPortalContent,
        widget = ReferenceBrowserWidget(
            allow_search = True,
            allow_browse = True,
            allow_sorting = True,
            show_indexes = False,
            force_close_on_insert = True,
            label = "Related Item(s)",
            label_msgid = "indfactsheet_label_related_items",
            description = "Specify relaetd item(s).",
            description_msgid = "indfactsheet_help_related_items",
            i18n_domain = "plone",
            visible = {'edit' : 'visible', 'view' : 'invisible' }
            )
        )

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

IndicatorFactSheet_schema = ATFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()
IndicatorFactSheet_schema.moveField('relatedItems', after='dpsir')

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class IndicatorFactSheet(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IIndicatorFactSheet)

    meta_type = 'IndicatorFactSheet'
    _at_rename_after_creation = True

    schema = IndicatorFactSheet_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(IndicatorFactSheet, PROJECTNAME)
# end of class IndicatorFactSheet

##code-section module-footer #fill in your manual code here
##/code-section module-footer



