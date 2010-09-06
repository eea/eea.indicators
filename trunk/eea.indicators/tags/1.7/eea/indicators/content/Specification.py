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
from Acquisition import aq_base, aq_inner, aq_parent
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import  ReferenceBrowserWidget
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes.atapi import *
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.utils import mapply
from Products.CMFCore import permissions
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.EEAContentTypes.content.ThemeTaggable import ThemeTaggable, ThemeTaggable_schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.UserAndGroupSelectionWidget import UserAndGroupSelectionWidget
from eea.dataservice.vocabulary import Organisations
from eea.indicators import msg_factory as _
from eea.indicators.browser.assessment import create_version as create_assessment_version
from eea.indicators.config import *
from eea.indicators.content.base import ModalFieldEditableAware, CustomizedObjectFactory
from eea.indicators.content.utils import get_dgf_value
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import has_versions, get_versions_api
from zope import event
from zope.app.event import objectevent
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
import datetime
import interfaces
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
        searchable=True,
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
        #allow_empty_rows=True,
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
                helper_js=("multiselectautocomplete_widget.js", ),
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
                description="Rationale uncertainty",
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
                description="Units",
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
                description="Methodology uncertainty",
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
                description="Data uncertainty",
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
                description="Methodology for gap filling",
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
                description="Related external indicator",
                label_msgid='indicators_label_related_external_indicator',
                i18n_domain='indicators',
                ),
            required=False,
            schemata="default",
            ),
    StringField(
            name='manager_user_id',
            widget= UserAndGroupSelectionWidget(
                label="The manager of this Indicator Specification",
                usersOnly=True,
                description="The manager of this Indicator Specification",
                label_msgid='indicators_label_manager_user_id',
                i18n_domain='indicators',
                ),
            schemata="default",
            required_for_published=True,
            ),
    EEAReferenceField(
            name='relatedItems',
            schemata='DataSpecs',
            relationship='relatesTo',
            multivalued=True,
            isMetadata=False,
            keepReferencesOnCopy=True,
            widget=EEAReferenceBrowserWidget(
                label='External data references',
                description="References to external data sets, available on other websites or via other organisations' communication channels.",
                label_msgid='indicators_label_specRelatedItems',
                description_msgid='indicators_help_specRelatedItems',
                macro="indicatorsrelationwidget",
                )),
            ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Specification_schema = ATFolderSchema.copy() + \
        getattr(ATFolder, 'schema', Schema(())).copy() + \
        schema.copy()

##code-section after-schema #fill in your manual code here

Specification_schema = Specification_schema + ThemeTaggable_schema.copy()
Specification_schema['themes'].schemata = 'Classification'
Specification_schema['themes'].required_for_published = True

#batch reorder of the fields
#this is created like this because we want explicit control over how the schemata fields
#are ordered and changing this in the UML modeler is just too time consuming
#TODO: get rid of this, we no longer use the UML modeler
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
finalizeATCTSchema(Specification_schema)


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

    portlet_readiness = ViewPageTemplateFile('../browser/templates/portlet_readiness.pt')

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

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDefinition()).getData()

    security.declarePublic("getTitle")
    def getTitle(self):
        """ Return title with codes.  """
        codes = self.getCodes()

        res = ''
        for code in codes:
            if code:
                res = res + "%s %s/" % (code['set'], code['code'])
        if res:
            res = self.title + ' (' + res[:-1] + ')'
        else:
            res = self.title
        return res

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
        """Returns a list of indicator codes, for indexing.

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

        #reindex all child assessment objects
        for assessment in self.objectValues('Assessment'):
            assessment.reindexObject()

    security.declarePublic('SearchableText')
    def SearchableText(self):
        """ """
        searchable_text = super(Specification, self).SearchableText()
        for code in self.get_codes():
            searchable_text += '%s ' % code.encode('utf-8')
        return searchable_text

    security.declarePublic('getMainCode')
    def getMainCode(self):
        """Returns the main code for this indicator (the first in the list of codes).
           Used for display purposed, like in title / description.
        """
        codes = self.getCodes()

        res = ''
        if len(codes)>0:
            code = codes[0]
            res = "%s %s" % (code['set'], code['code'])
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

    def factory_MethodologyReference(self):
        type_name = 'MethodologyReference'
        return self._generic_factory(type_name)

    def factory_Assessment(self):
        type_name = 'Assessment'

        create = self.REQUEST.form.get('create_in_latest_spec')
        if create == 'true':
            info = IGetVersions(self)
            latest = info.latest_version()
            if latest.UID() != self.UID():
                return latest.factory_Assessment()

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

        # if there are no other assessments in this version set we look for other
        # IndicatorFactSheet objects with same indicator code to get the versionId
        if not version_id:
            brains = []
            codes = self.get_codes()
            cat = getToolByName(self, 'portal_catalog')
            for code in codes[1::2]:
                brains = cat.searchResults({'portal_type': 'IndicatorFactSheet',
                                            'get_codes': code})
                if brains:
                    break
            if brains:
                version_id = IVersionControl(brains[0].getObject()).versionId

        #create a new Assessment from scratch
        #id = self.generateUniqueId(type_name)
        id = make_id('assessment', self.objectIds())
        new_id = self.invokeFactory(type_name=type_name,
                id=id,
                base_impl=True,
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

        ast.reindexObject()
        return {'obj':ast, 'subview':'@@edit_aggregated', 'direct_edit':True}

    def has_newer_version(self):
        versions = get_versions_api(self)
        newest = versions.newest()

        if has_versions(self) and newest:
            return True
        return False

    security.declareProtected(AddPortalContent, 'invokeFactory')
    def invokeFactory(self, type_name, id, RESPONSE=None, base_impl=False, *args, **kw):
        if base_impl:
            return super(Specification, self).invokeFactory(type_name, id, RESPONSE, *args, **kw)
        factory_name = 'factory_' + type_name
        factory = getattr(self, factory_name, None)
        obj = factory()['obj']
        return obj.getId()


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
