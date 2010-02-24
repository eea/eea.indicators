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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
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
        required=True,
        schemata="default",
        accessor="Title",
    ),
    DateTimeField(
        name='version',
        widget=DateTimeField._properties['widget'](
            label="Version",
            label_msgid='indicators_label_version',
            i18n_domain='indicators',
        ),
        schemata="default",
    ),
    DataGridField(
        name='codes',
        widget=DataGridWidget(
            label="Specification identification codes",
            columns={'set':Column("Set ID"), "code":Column("Code number")},
            label_msgid='indicators_label_codes',
            i18n_domain='indicators',
        ),
        schemata="default",
        columns=("set", "code"),
    ),
    StringField(
        name='source_code',
        widget=StringField._properties['widget'](
            label="Source Code",
            description="Useful only for CSI indicators, to tell which was original code",
            label_msgid='indicators_label_source_code',
            description_msgid='indicators_help_source_code',
            i18n_domain='indicators',
        ),
        schemata="default",
    ),
    TextField(
        name='more_updates_on',
        widget=TextAreaWidget(
            label="More updates on",
            label_msgid='indicators_label_more_updates_on',
            i18n_domain='indicators',
        ),
        schemata="default",
    ),
    StringField(
        name='dpsir',
        widget=SelectionWidget(
            label="DPSIR",
            label_msgid='indicators_label_dpsir',
            i18n_domain='indicators',
        ),
        schemata="Classification",
    ),
    StringField(
        name='typology',
        widget=SelectionWidget(
            label="Typology",
            label_msgid='indicators_label_typology',
            i18n_domain='indicators',
        ),
        schemata="Classification",
    ),
    StringField(
        name='csi_topics',
        widget=SelectionWidget(
            label="CSI Topics",
            label_msgid='indicators_label_csi_topics',
            i18n_domain='indicators',
        ),
        schemata="Classification",
    ),
    LinesField(
        name='themes',
        widget=LinesField._properties['widget'](
            label="Themes",
            label_msgid='indicators_label_themes',
            i18n_domain='indicators',
        ),
        schemata="Classification",
    ),
    StringField(
        name='eea_indicator_manager',
        widget=SelectionWidget(
            label="EEA Indicator Manager",
            label_msgid='indicators_label_eea_indicator_manager',
            i18n_domain='indicators',
        ),
        schemata="Responsability",
    ),
    LinesField(
        name='ownership',
        widget=LinesField._properties['widget'](
            label="Ownership",
            label_msgid='indicators_label_ownership',
            i18n_domain='indicators',
        ),
        schemata="Responsability",
    ),
    StringField(
        name='manager_user_id',
        widget=StringField._properties['widget'](
            label="ID of manager user",
            label_msgid='indicators_label_manager_user_id',
            i18n_domain='indicators',
        ),
        schemata="Responsability",
    ),
    StringField(
        name='csi_status',
        widget=SelectionWidget(
            label="CSI Status",
            label_msgid='indicators_label_csi_status',
            i18n_domain='indicators',
        ),
        schemata="Status",
    ),
    TextField(
        name='comment',
        widget=TextAreaWidget(
            label="Comments",
            label_msgid='indicators_label_comment',
            i18n_domain='indicators',
        ),
        schemata="Status",
    ),
    TextField(
        name='rationale_justification',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Rationale justification",
            label_msgid='indicators_label_rationale_justification',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="Rationale",
    ),
    TextField(
        name='rational_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Rationale uncertainty",
            label_msgid='indicators_label_rational_uncertainty',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="Rationale",
    ),
    TextField(
        name='policy_context_description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Policy context",
            label_msgid='indicators_label_policy_context_description',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="PolicyContext",
    ),
    TextField(
        name='policy_context_targets',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Targets for the policy context",
            label_msgid='indicators_label_policy_context_targets',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="PolicyContext",
    ),
    LinesField(
        name='related_policy_documents',
        widget=LinesField._properties['widget'](
            label="Related Policy Documents",
            label_msgid='indicators_label_related_policy_documents',
            i18n_domain='indicators',
        ),
        schemata="PolicyContext",
    ),
    StringField(
        name='version_id',
        widget=StringField._properties['widget'](
            label="Version ID",
            label_msgid='indicators_label_version_id',
            i18n_domain='indicators',
        ),
        required=True,
        schemata="default",
        description="A unique sequence of characters that is shared by all the specifications which are versions of each other",
    ),
    BooleanField(
        name='published_on_eea',
        widget=BooleanField._properties['widget'](
            label="Published on EEA?",
            label_msgid='indicators_label_published_on_eea',
            i18n_domain='indicators',
        ),
        schemata="default",
    ),
    DateTimeField(
        name='publish_date',
        widget=DateTimeField._properties['widget'](
            label="Publication date",
            label_msgid='indicators_label_publish_date',
            i18n_domain='indicators',
        ),
        schemata="default",
    ),
    ReferenceField(
        name='externaldataspecs',
        widget=ReferenceBrowserWidget(
            label='Externaldataspecs',
            label_msgid='indicators_label_externaldataspecs',
            i18n_domain='indicators',
        ),
        allowed_types=('ExternalDataSpec',),
        multiValued=1,
        relationship='has_external_data_specs',
    ),
    ReferenceField(
        name='eeadatas',
        widget=ReferenceBrowserWidget(
            label='Eeadatas',
            label_msgid='indicators_label_eeadatas',
            i18n_domain='indicators',
        ),
        allowed_types=('EEAData',),
        multiValued=1,
        relationship='has_eea_data_specs',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Specification_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Specification(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISpecification)

    meta_type = 'Specification'
    _at_rename_after_creation = True

    schema = Specification_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Specification, PROJECTNAME)
# end of class Specification

##code-section module-footer #fill in your manual code here
##/code-section module-footer



