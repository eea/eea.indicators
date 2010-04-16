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
from Products.ATVocabularyManager import NamedVocabulary

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.Archetypes.utils import mapply
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.EEAContentTypes.content.ThemeTaggable import ThemeTaggable, ThemeTaggable_schema
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.UserAndGroupSelectionWidget import UserAndGroupSelectionWidget
from eea.dataservice.vocabulary import Organisations
from eea.indicators import msg_factory as _
from eea.indicators.browser.assessment import create_version as create_assessment_version
from eea.indicators.content.base import ModalFieldEditableAware, CustomizedObjectFactory
from zope import event
from zope.app.event import objectevent

import datetime
import logging

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
        schemata="default",
        searchable=True,
        required=True,
        accessor="getTitle",
        required_for_published=True,
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
            columns={'set':SelectColumn("Set ID", vocabulary="get_indicator_codes"), "code":Column("Code number")},
            auto_insert=True,
            label_msgid='indicators_label_codes',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        columns=("set", "code"),
        required_for_published=True,
    ),
    TextField(
        name='more_updates_on',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="More updates on",
            label_msgid='indicators_label_more_updates_on',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="default",
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='dpsir',
        widget=SelectionWidget(
            label="DPSIR",
            label_msgid='indicators_label_dpsir',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        vocabulary=[("None", ""), ('D', 'Driving forces'), ('P', 'Pressures'), ('S', 'States'), ('I', 'Impacts'), ('R', 'Reactions')],
        required_for_published=True,
    ),
    StringField(
        name='typology',
        widget=SelectionWidget(
            label="Typology",
            label_msgid='indicators_label_typology',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        vocabulary=[['None', ''], ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E']],
        required_for_published=True,
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
        default_content_type="text/html",
        searchable=True,
        schemata="Responsability",
        default_output_type="text/x-html-safe",
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
        widget=RichWidget(
            label="Rationale justification",
            label_msgid='indicators_label_rationale_justification',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        schemata="Rationale",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='rationale_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Rationale uncertainty",
            label_msgid='indicators_label_rationale_uncertainty',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="Rationale",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='policy_context_description',
        widget=RichWidget(
            label="Policy context",
            label_msgid='indicators_label_policy_context_description',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        schemata="PolicyContext",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='policy_context_targets',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Targets for the policy context",
            label_msgid='indicators_label_policy_context_targets',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="PolicyContext",
        default_output_type="text/x-html-safe",
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
        widget=RichWidget(
            label="Definition",
            label_msgid='indicators_label_definition',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=False,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        schemata="default",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='units',
        widget=RichWidget(
            label="Units",
            label_msgid='indicators_label_units',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=False,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        schemata="default",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='methodology',
        widget=RichWidget(
            label="Methodology",
            label_msgid='indicators_label_methodology',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=False,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        schemata="Methodology",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='methodology_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Methodology uncertainty",
            label_msgid='indicators_label_methodology_uncertainty',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="Methodology",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='data_uncertainty',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Data uncertainty",
            label_msgid='indicators_label_data_uncertainty',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="DataSpecs",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='methodology_gapfilling',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Methodology gapfilling",
            label_msgid='indicators_label_methodology_gapfilling',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="Methodology",
        default_output_type="text/x-html-safe",
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
    StringField(
        name='manager_user_id',
        widget=StringField._properties['widget'](
            label="Indicator Manager User",
            label_msgid='indicators_label_manager_user_id',
            i18n_domain='indicators',
        ),
        schemata="default",
        required_for_published=True,
    ),
    ReferenceField(
        name='relatedItems',
        widget=ReferenceBrowserWidget(
            label="External data sets",
            addable=True,
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
            addable=True,
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
            addable=True,
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
            addable=True,
            destination="./../",
            label_msgid='indicators_label_related_policy_documents',
            i18n_domain='indicators',
        )

Specification_schema['manager_user_id'].widget = UserAndGroupSelectionWidget(
            label="The manager of this Indicator Specification",
            usersOnly=True,
            label_msgid='indicators_label_manager_user_id',
            i18n_domain='indicators',
        )

Specification_schema['themes'].schemata = 'Classification'

#batch reorder of the fields
#this is created like this because we want explicit control over how the schemata fields
#are ordered and changing this in the UML modeler is just too time consuming
_field_order = [
        {
            'name':'default',
            'fields':[  'title', 'description', 'more_updates_on', 'definition',
                        'units', 'related_external_indicator', 'manager_user_id']
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
            'fields':['version', 'codes', 'dpsir', 'typology', 'csi_topics', 'version_id', 'themes']
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
Specification_schema['themes'].required_for_publication = True
finalizeATCTSchema(Specification_schema)

required_for_publication = [
                            "title",
                            "codes",
                            "dpsir",
                            "typology",
                            "rationale_justification",
                            "policy_context_description",
                            "definition",
                            "units",
                            "methodology",
                            "manager_user_id",
                            "themes",
                            ]

##/code-section after-schema

class Specification(ATFolder, ThemeTaggable,  ModalFieldEditableAware,  CustomizedObjectFactory, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISpecification)

    meta_type = 'Specification'
    _at_rename_after_creation = True

    schema = Specification_schema

    ##code-section class-header #fill in your manual code here

    #this template is customized to expose the number of remaining
    #unfilled fields that are mandatory for publishing
    edit_macros = PageTemplateFile('edit_macros.pt', templates_dir)

    ##/code-section class-header

    # Methods

    # Manually created methods

    def get_work(self):
        in_future = datetime.datetime.now() + ONE_YEAR
        items = self.objectValues('WorkItem')
        short_term = []
        long_term = []
        incomplete = []
        for item in items:
            d = item.getDue_date()
            if not(d):
                incomplete.append(item)
                continue
            date = datetime.datetime(d.year(), d.month(), d.day())
            if date > in_future:
                long_term.append(item)
            else:
                short_term.append(item)
        return {'long':long_term, 'short':short_term, 'incomplete':incomplete}

    security.declareProtected(permissions.View, 'getOrganisationName')
    def getOrganisationName(self, url):
        """ """
        res = None
        cat = getToolByName(self, 'portal_catalog')
        brains = cat.searchResults({'portal_type' : 'Organisation',
                                    'getUrl': url})
        if brains: res = brains[0]
        return res

    security.declarePublic("Title")
    def Title(self):
        has_versions = self.unrestrictedTraverse('@@hasVersions')()

        if not has_versions:
            return self.getTitle()

        version = 0 #avoids problem in create new version
        versions = self.unrestrictedTraverse('@@getVersions')()

        for k,v in versions.items():    #this is a dict {1:<Spec>, 2:<Spec>}
            if v.getPhysicalPath() == self.getPhysicalPath():
                version = k
                break

        msg = _(u"specification_title_msg",
                default=u"${title} (version ${version})",
                mapping={'title':self.getTitle(), 'version':version})

        return self.translate(msg)

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDefinition()).getData()

    security.declarePublic('get_completeness')
    def get_completeness(self):

        _done           = 0 #the percentage of fields required for publication that are filled in
        _optional       = 0 #fields that are not required for publication that are not filled in
        _required       = 0 #the fields required for publication that are filled in
        _total_required = 0 #the number of fields that are required for publication
        _total          = 0 #the grand total of fields

        for field in self.schema.fields():
            _total += 1
            has_value = bool(field.getAccessor(self)())  #we assume that the return value is something not empty

            if getattr(field, 'required_for_publication', False):
                _total_required += 1
                if has_value:
                    _required += 1
            else:
                if not has_value:
                    _optional += 1

        _done = int(float(_required) / float(_total_required) * 100.0)

        return {
                'done':_done,
                'required':_required,
                'publishing':_total_required,
                'optional':_optional,
                'total':_total,
                }
    security.declarePublic('left_slots')
    def left_slots(self):
        _slot = ['here/portlet_readiness/macros/portlet']
        #_assigned = self.getProperty('left_slots') or []

        parent = self.aq_parent
        base_slots=getattr(parent,'left_slots', [])
        if callable(base_slots):
            base_slots = base_slots()

        return list(base_slots) + _slot

    def get_indicator_codes(self):
        atvm = getToolByName(self, ATVOCABULARYTOOL)
        vocab = getattr(atvm, 'indicator_codes')
        return vocab.getDisplayList(self)

    security.declarePublic('get_codes')
    def get_codes(self):
        """Returns a list of specification codes, for indexing.

        Indexes the codes of this specification in the form of
        a KeywordIndex with ['SETA', "SETA001", "SETB", "SETB009"]
        the idea is to be able to search for set code (ex: SETB)
        but also for the full code (ex:SETB009)
        """
        codes = self.getCodes()
        res = []
        for code in codes:
            res.extend(
                [code['set'],
                "%s%s" % (code['set'], code['code'])]
                )
        return res

    def factory_RationaleReference(self):
        type_name = 'RationaleReference'
        return self._generic_factory(type_name)

    def factory_PolicyQuestion(self):
        type_name = 'PolicyQuestion'
        return self._generic_factory(type_name)

    def factory_WorkItem(self):
        type_name = 'WorkItem'
        return self._generic_factory(type_name)

    def factory_Assessment(self):
        type_name = 'Assessment'

        #create a version if we already have an Assessment
        assessments = self.objectValues(type_name)
        if assessments:
            original = assessments[-1]  #we assume the latest object is the last one
            return create_assessment_version(original)

        #create a new Assessment from scratch
        id = self.generateUniqueId(type_name)
        new_id = self.invokeFactory(type_name=type_name,
                id=id,
                title=self.translate(
                    msgid='label-newly-created-type',
                    domain='indicators',
                    default="Newly created ${type_name}",
                    mapping={'type_name':type_name},
                    ))
        ast = self[new_id]

        #create assessment parts for each policy question
        for pq in self.objectValues("PolicyQuestion"):
            id = ast.invokeFactory(type_name="AssessmentPart",
                    id=ast.generateUniqueId("PolicyQuestion"),)
            ap = ast[id]
            ap.setQuestion_answered(pq)
            ap.reindexObject()

        return ast



registerType(Specification, PROJECTNAME)
# end of class Specification

##code-section module-footer #fill in your manual code here

#placed here so that it will be found by extraction utility
_titlemsg = _('label-newly-created-type',
        default="Newly created ${type_name}",
        )

##/code-section module-footer



