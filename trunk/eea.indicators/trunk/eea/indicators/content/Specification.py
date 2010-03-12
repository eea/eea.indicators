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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from Products.Archetypes.atapi import MultiSelectionWidget

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.EEAContentTypes.content.ThemeTaggable import ThemeTaggable, ThemeTaggable_schema
from eea.dataservice.vocabulary import Organisations

import datetime

ONE_YEAR = datetime.timedelta(weeks=52)
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
        searchable=True,
    ),
    DateTimeField(
        name='version',
        widget=DateTimeField._properties['widget'](
            label="Version",
            label_msgid='indicators_label_version',
            i18n_domain='indicators',
        ),
        schemata="Classification",
    ),
    DataGridField(
        name='codes',
        widget=DataGridWidget(
            label="Specification identification codes",
            columns={'set':Column("Set ID"), "code":Column("Code number")},
            label_msgid='indicators_label_codes',
            i18n_domain='indicators',
        ),
        schemata="Classification",
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
        schemata="Classification",
    ),
    TextField(
        name='more_updates_on',
        widget=TextAreaWidget(
            label="More updates on",
            label_msgid='indicators_label_more_updates_on',
            i18n_domain='indicators',
        ),
        schemata="default",
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
    ),
    StringField(
        name='typology',
        widget=SelectionWidget(
            label="Typology",
            label_msgid='indicators_label_typology',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        vocabulary=['A','B','C','D', 'E'],
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
        name='ownership',
        widget=MultiSelectionWidget(
            label="Owner",
            macro="organisations_widget",
            label_msgid='indicators_label_ownership',
            i18n_domain='indicators',
        ),
        schemata="Responsability",
        vocabulary=Organisations(),
    ),
    TextField(
        name='contact',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="ID of manager user",
            label_msgid='indicators_label_contact',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="Responsability",
        searchable=True,
    ),
    StringField(
        name='csi_status',
        widget=SelectionWidget(
            label="CSI Status",
            visible={'view':'hidden', 'edit':'hidden'},
            label_msgid='indicators_label_csi_status',
            i18n_domain='indicators',
        ),
        schemata="default",
        vocabulary=["Under development", "Proposed for core set", "Endorsed by management board", "Dropped from core set"],
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
        searchable=True,
    ),
    TextField(
        name='rationale_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Rationale uncertainty",
            label_msgid='indicators_label_rationale_uncertainty',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="Rationale",
        searchable=True,
    ),
    TextField(
        name='policy_context_description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Policy context",
            label_msgid='indicators_label_policy_context_description',
            i18n_domain='indicators',
        ),
        required=True,
        schemata="PolicyContext",
        searchable=True,
        default_output_type='text/html',
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
        searchable=True,
    ),
    StringField(
        name='version_id',
        widget=StringField._properties['widget'](
            label="Version ID",
            label_msgid='indicators_label_version_id',
            i18n_domain='indicators',
        ),
        required=True,
        schemata="Classification",
        description="A unique sequence of characters that is shared by all the specifications which are versions of each other",
        searchable=True,
    ),
    StringField(
        name='old_id',
        widget=StringField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
            label='Old_id',
            label_msgid='indicators_label_old_id',
            i18n_domain='indicators',
        ),
        searchable=True,
    ),
    TextField(
        name='definition',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Definition",
            label_msgid='indicators_label_definition',
            i18n_domain='indicators',
        ),
        required=False,
        schemata="default",
        searchable=True,
        default_output_type='text/html',
    ),
    TextField(
        name='units',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Units",
            label_msgid='indicators_label_units',
            i18n_domain='indicators',
        ),
        required=False,
        schemata="default",
        searchable=True,
        default_output_type='text/html',
    ),
    TextField(
        name='methodology',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Methodology",
            label_msgid='indicators_label_methodology',
            i18n_domain='indicators',
        ),
        required=False,
        schemata="Methodology",
        searchable=True,
        default_output_type='text/html',
    ),
    TextField(
        name='methodology_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Methodology uncertainty",
            label_msgid='indicators_label_methodology_uncertainty',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="Methodology",
        searchable=True,
    ),
    TextField(
        name='data_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Data uncertainty",
            label_msgid='indicators_label_data_uncertainty',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="DataSpecs",
        searchable=True,
    ),
    TextField(
        name='methodology_gapfilling',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Methodology gapfilling",
            label_msgid='indicators_label_methodology_gapfilling',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        schemata="Methodology",
        searchable=True,
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            visible={'view':'invisible', 'edit':'invisible'},
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='related_external_indicator',
        widget=StringField._properties['widget'](
            label="Related external indicator",
            label_msgid='indicators_label_related_external_indicator',
            i18n_domain='indicators',
        ),
        required=False,
        schemata="default",
    ),
    ReferenceField(
        name='relatedItems',
        widget=ReferenceBrowserWidget(
            label="External data sets",
            addable="True",
            label_msgid='indicators_label_relatedItems',
            i18n_domain='indicators',
        ),
        allowed_types=('ExternalDataSpec',),
        schemata="DataSpecs",
        multiValued=1,
        relationship='specification_relateditems',
    ),
    ReferenceField(
        name='specification_data',
        widget=ReferenceBrowserWidget(
            label="Datasets used for this Specification",
            label_msgid='indicators_label_specification_data',
            i18n_domain='indicators',
        ),
        allowed_types=('Data',),
        schemata="DataSpecs",
        multiValued=1,
        relationship='specification_specification_data',
    ),
    ReferenceField(
        name='related_policy_documents',
        widget=ReferenceBrowserWidget(
            label="Related Policy Documents",
            addable="True",
            destination="./../",
            label_msgid='indicators_label_related_policy_documents',
            i18n_domain='indicators',
        ),
        allowed_types=('PolicyDocumentReference',),
        schemata="PolicyContext",
        multiValued=1,
        relationship='specification_related_policy_documents',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Specification_schema = ATFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Specification_schema = Specification_schema + ThemeTaggable_schema.copy()

Specification_schema['relatedItems'].widget = ReferenceWidget(
            label="External data sets",
            addable="True",
            label_msgid='indicators_label_relatedItems',
            i18n_domain='indicators',
        )

Specification_schema['specification_data'].widget = ReferenceWidget(
            label="Datasets used for this Specification",
            label_msgid='indicators_label_specification_data',
            i18n_domain='indicators',
        )

Specification_schema['related_policy_documents'].widget = ReferenceWidget(
            label="Related Policy Documents",
            addable="True",
            destination="./../",
            label_msgid='indicators_label_related_policy_documents',
            i18n_domain='indicators',
        )

Specification_schema['themes'].schemata = 'Classification'

#batch reorder of the fields
#this is created like this because we want explicit control over how the schemata fields
#are ordered and changing this in the UML modeler is just too time consuming
_field_order = [
        {
            'name':'default',
            'fields':['title', 'description', 'more_updates_on', 'definition', 'units', 'related_external_indicator',]
            },
        {
            'name':'Rationale',
            'fields':['rationale_justification', 'rationale_uncertainty',]
            },
        {
            'name':'PolicyContext',
            'fields':['policy_context_description', 'policy_context_targets', 'related_policy_documents', ]
            },
        {
            'name':'Methodology',
            'fields':['methodology', 'methodology_uncertainty', 'methodology_gapfilling', ]
            },
        {
            'name':'DataSpecs',
            'fields':['relatedItems', 'data_uncertainty', 'specification_data',]
            },
        {
            'name':'Classification',
            'fields':['version', 'codes', 'source_code', 'dpsir', 'typology', 'csi_topics', 'version_id', 'themes']
            },
        {
            'name':'Responsability',
            'fields':['ownership', 'contact', ]
            },
        ]

old_order = Specification_schema._names
new_order = []
for info in _field_order:
    new_order.extend(info['fields'])

for name in old_order:  #add fields that are not in our specified list at the end of the schema
    if name not in new_order:
        new_order.append(name)

Specification_schema._names = new_order
finalizeATCTSchema(Specification_schema)
##/code-section after-schema

class Specification(ATFolder, ThemeTaggable, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISpecification)

    meta_type = 'Specification'
    _at_rename_after_creation = False

    schema = Specification_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def get_work(self):
        in_future = datetime.datetime.now() + ONE_YEAR
        items = self.objectValues('WorkItem')
        short_term = []
        long_term = []
        for item in items:
            d = item.getDue_date()
            date = datetime.datetime(d.year(), d.month(), d.day())
            if date > in_future:
                long_term.append(item)
            else:
                short_term.append(item)
        return {'long':long_term, 'short':short_term}

    security.declareProtected(permissions.View, 'getOrganisationName')
    def getOrganisationName(self, url):
        """ """
        res = None
        cat = getToolByName(self, 'portal_catalog')
        brains = cat.searchResults({'portal_type' : 'Organisation',
                                    'getUrl': url})
        if brains: res = brains[0]
        return res

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDefinition()).getData()



registerType(Specification, PROJECTNAME)
# end of class Specification

##code-section module-footer #fill in your manual code here
##/code-section module-footer



