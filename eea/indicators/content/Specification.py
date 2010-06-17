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
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary

##code-section module-header #fill in your manual code here
from Acquisition import aq_base, aq_inner, aq_parent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.Archetypes.utils import mapply
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.EEAContentTypes.content.ThemeTaggable import ThemeTaggable, ThemeTaggable_schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.UserAndGroupSelectionWidget import UserAndGroupSelectionWidget
from eea.dataservice.vocabulary import Organisations
from eea.indicators import msg_factory as _
from eea.indicators.browser.assessment import create_version as create_assessment_version
from eea.indicators.content.base import ModalFieldEditableAware, CustomizedObjectFactory
from eea.indicators.content.utils import get_dgf_value
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from zope import event
from zope.app.event import objectevent
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
import datetime
import logging

ONE_YEAR = datetime.timedelta(weeks=52)
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Title",
            description="The generic title of the indicator which is stable over a long period. It is short enough to explain the tracked issue and it does not contain specific dates.",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        schemata="default",
        searchable=True,
        default="Untitled indicator",
        required=True,
        accessor="getTitle",
        required_for_published=True,
    ),
    DataGridField(
        name='codes',
        widget=DataGridWidget(
            label="Specification identification codes",
            description="Codes are short names used to identify the indicator in question. Code is made up of a SET-ID and an CODE-NR, e.g. TERM 002. Multiple codes are allowed, since same indicator can be re-used in other indicators' sets.",
            columns={'set':SelectColumn("Set ID", vocabulary="get_indicator_codes"), "code":Column("Code number")},
            auto_insert=True,
            label_msgid='indicators_label_codes',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        columns=("set", "code"),
        required_for_published=True,
        validators=('unique_specification_code',),
    ),
    TextField(
        name='more_updates_on',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Message info on updates",
            description="This information is used to display warning messages to the users on top of the indicator page.",
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
            label="Position in DPSIR framework",
            description="The work of the EEA is built around a conceptual framework known as the DPSIR assessment framework. DPSIR stands for ‘driving forces, pressures, states, impacts and responses’. DPSIR builds on the existing OECD model and offers a basis for analysing the interrelated factors that impact on the environment.",
            label_msgid='indicators_label_dpsir',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        vocabulary=NamedVocabulary("indicator_dpsir"),
        required_for_published=True,
    ),
    StringField(
        name='typology',
        widget=SelectionWidget(
            label="Typology",
            description="Typology is a categorisation based on a simple set of questions: what is happening (A) is this relevant (B) can we make progress in improving the way we do things (C), are the undertaken policy measures effective (Type D) and does this contribute to our overall welfare (E)?, led to a first typology of indicators. The typology was used to demonstrate that (in",
            label_msgid='indicators_label_typology',
            i18n_domain='indicators',
        ),
        schemata="Classification",
        vocabulary=NamedVocabulary("indicator_typology"),
        required_for_published=True,
    ),
    LinesField(
        name='ownership',
        widget=MultiSelectionWidget(
            label="Owners",
            description="One or several institutions/organisations sharing ownership for this indicator.",
            macro="organisations_widget",
            label_msgid='indicators_label_ownership',
            i18n_domain='indicators',
        ),
        schemata="Responsability",
        vocabulary=Organisations(),
        required=True,
        required_for_published=True,
    ),
    TextField(
        name='rationale_justification',
        widget=RichWidget(
            label="Rationale for indicator selection",
            description="Explanation and justification of indicator selection.",
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
            description="Policy context is the main driving force for presentation of indicator and its assessments.",
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
            description="A quantitative value which usually underpins a European Union or other international policy objective. The target usually has a time deadline that should be met through the design and implementation of measures by countries.",
            label_msgid='indicators_label_policy_context_targets',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="PolicyContext",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='definition',
        widget=RichWidget(
            label="Definition",
            description="Provide short textual definition of the indicator. Provide units and list of parameters, sectors, media, processes used in indicator. A definition is a statement of the precise meaning of something. Often includes specific examples of what is and is not included in particular categories. ",
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
            label="Methodology for indicator calculation",
            description="Guidelines for calculating the indicator, including exact formulas and/or links to more explanatory methodological description",
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
            label="Methodology for gap filling",
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
            description='A short and concise description about this indicator.',
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
            label="EEA Indicator Manager",
            description="Central contact point for this indicator, mainly responsible for the indicator update and its further development.",
            label_msgid='indicators_label_manager_user_id',
            i18n_domain='indicators',
        ),
        schemata="default",
        required_for_published=True,
    ),
    ReferenceField(
        name='relatedItems',
        widget=ReferenceBrowserWidget(
            label="External data references",
            addable=True,
            description="References to external data sets, available on other websites or via other organisations' communication channels.",
            label_msgid='indicators_label_relatedItems',
            description_msgid='indicators_help_relatedItems',
            i18n_domain='indicators',
            keepReferencesOnCopy=True,
        ),
        allowed_types=('ExternalDataSpec',),
        schemata="DataSpecs",
        multiValued=1,
        relationship='specification_relateditems',
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

Specification_schema['relatedItems'] = EEAReferenceField('relatedItems',
        schemata='DataSpecs',
        relationship='relatesTo',
        multivalued=True,
        isMetadata=False,
        widget=EEAReferenceBrowserWidget(
            label='External data references',
            description="References to external data sets, available on other websites or via other organisations' communication channels.",
            label_msgid='indicators_label_specRelatedItems',
            description_msgid='indicators_help_specRelatedItems',
            macro="indicatorsrelationwidget",
            ))

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
            'fields':['policy_context_description', 'policy_context_targets',]
            },
        {
            'name':'Methodology',
            'fields':['methodology', 'methodology_uncertainty', 'methodology_gapfilling',]
            },
        {
            'name':'DataSpecs',
            'fields':['relatedItems', 'data_uncertainty']
            },
        {
            'name':'Classification',
            'fields':['codes', 'dpsir', 'typology', 'themes']
            },
        {
            'name':'Responsability',
            'fields':['ownership']
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

    def get_assessments(self):
        assessments = self.objectValues('Assessment')
        pass

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

        getVersions = self.unrestrictedTraverse('@@getVersions')
        version = getVersions.version_number()

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
        _slot = 'here/portlet_readiness/macros/portlet'
        #_assigned = self.getProperty('left_slots') or []

        parent = aq_parent(aq_inner(self))
        base_slots=getattr(parent,'left_slots', [])
        if callable(base_slots):
            base_slots = base_slots()

        base_slots = list(base_slots)
        base_slots.insert(0, _slot)
        return base_slots

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
            if code:
                res.extend(
                    [code['set'],
                    "%s%s" % (code['set'], code['code'])]
                    )
        return res

    security.declareProtected("Modify portal content", 'setCodes')
    def setCodes(self, value):
        #we want to filter rows that don't have a number filled in
        field = self.schema['codes']
        instance = self
        value = get_dgf_value(field, value)
        for row in value:
            try:
                row['code'] = "%03d" % int(row['code'])
            except ValueError:
                continue
        field.getStorage(instance).set(field.getName(), instance, value)

    def factory_RationaleReference(self):
        type_name = 'RationaleReference'
        return self._generic_factory(type_name)

    def factory_PolicyQuestion(self):
        type_name = 'PolicyQuestion'
        return self._generic_factory(type_name)

    def factory_WorkItem(self):
        type_name = 'WorkItem'
        return self._generic_factory(type_name)

    def factory_MethodologyReference(self):
        type_name = 'MethodologyReference'
        return self._generic_factory(type_name)

    def factory_Assessment(self):
        type_name = 'Assessment'

        #drop with error if no PolicyQuestions are created
        if not self.objectValues('PolicyQuestion'):
            return self.error("You need to create first a Policy Question")

        #create a version if we already have an Assessment
        assessments = self.objectValues(type_name)
        if assessments:
            original = assessments[-1]  #NOTE: we assume the latest object is the last one
            ast = create_assessment_version(original)
            return {'obj':ast, 'subview':'@@edit_aggregated', 'direct_edit':True}

        #we want to make this assessment a version of a previous assessment
        #if this Specification is already versioned, so we try get a versionId

        version_id = None
        spec_versions = self.unrestrictedTraverse('@@getVersions')().values()
        for spec in spec_versions:
            asts = spec.objectValues("Assessment")
            if asts:
                original = asts[0]
                version_id = IVersionControl(original).versionId
                break

        #create a new Assessment from scratch
        #id = self.generateUniqueId(type_name)
        id = make_id('assessment', self.objectIds())
        new_id = self.invokeFactory(type_name=type_name,
                id=id,
                title=self.translate(
                    msgid='label-newly-created-type',
                    domain='indicators',
                    default="Newly created ${type_name}",
                    mapping={'type_name':type_name},
                    ))
        ast = self[new_id]

        if version_id:
            IVersionControl(ast).setVersionId(version_id)
            alsoProvides(ast, IVersionEnhanced)

        #create assessment parts for each policy question
        for pq in self.objectValues("PolicyQuestion"):
            id = ast.invokeFactory(type_name="AssessmentPart",
                                   id=ast.generateUniqueId("AssessmentPart"),)
            ap = ast[id]
            ap.setRelatedItems(pq)
            ap.reindexObject()

        return {'obj':ast, 'subview':'@@edit_aggregated', 'direct_edit':True}

    def has_newer_version(self):
        versions = getMultiAdapter((self, self.REQUEST), name="getVersions")
        has_versions = getMultiAdapter((self, self.REQUEST), name="getVersions")()

        newest = versions.newest()
        if has_versions and newest:
            return True

        return False

    #security.declarePublic('portlet_readiness')
    #def portlet_readiness(self):
    portlet_readiness = ViewPageTemplateFile('../browser/templates/portlet_readiness.pt')


registerType(Specification, PROJECTNAME)
# end of class Specification

##code-section module-footer #fill in your manual code here

#placed here so that it will be found by extraction utility
_titlemsg = _('label-newly-created-type',
        default="Newly created ${type_name}",
        )


def make_id(BASE, names):
    """Useful in making a unique id in a container

    Given a BASE such as 'assessment' and a list of ids, it returns
    the first string such as assessmenet-10 that is not found in the list of ids
    """
    x = 1
    name = None

    if BASE not in names:
        name = BASE
    else:
        while True:
            name = "%s-%s" % (BASE, x)
            if name not in names:
                break
            x += 1

    return name

##/code-section module-footer
