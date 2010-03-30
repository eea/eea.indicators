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
        vocabulary=['A','B','C','D', 'E'],
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
        schemata="Rationale",
        searchable=True,
        default_output_type='text/html',
        required_for_published=True,
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
        required_for_published=True,
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
        required_for_published=True,
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
        required_for_published=True,
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
        required_for_published=True,
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

class Specification(ATFolder, ThemeTaggable, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISpecification)

    meta_type = 'Specification'
    _at_rename_after_creation = False

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

    security.declareProtected(permissions.ModifyPortalContent, 'object_factory')
    def object_factory(self):
        """Create an object according to special rules for that object """

        factories = SpecificationFactories(self)
        type_name = self.REQUEST['type_name']
        factory = factories[type_name]
        obj = factory()
        return "OK"

    security.declareProtected(permissions.ModifyPortalContent, 'delete_object')
    def delete_object(self):
        """Delete objects from this container"""

        id = self.REQUEST['id']
        del self[id]
        return "OK"

    security.declareProtected(permissions.ModifyPortalContent, 'simpleProcessForm')
    def simpleProcessForm(self, data=1, metadata=0, REQUEST=None, values=None):
        """Processes the schema looking for data in the form.
        """

        #customized to process a single field instead of multiple fields

        request = REQUEST or self.REQUEST
        _marker = []
        if values:
            form = values
        else:
            form = request.form

        fieldset = form.get('fieldset', None)
        schema = self.Schema()
        schemata = self.Schemata()
        fields = []

        fieldname = None
        for name in form.keys():
            if name in self.schema.keys():
                fieldname = name

        if not fieldname:
            raise ValueError("Field is not found")
            return

        field = self.schema[fieldname]

        result = field.widget.process_form(self, field, form,
                                           empty_marker=_marker)
        try:
            # Pass validating=False to inform the widget that we
            # aren't in the validation phase, IOW, the returned
            # data will be forwarded to the storage
            result = field.widget.process_form(self, field, form,
                                               empty_marker=_marker,
                                               validating=False)
        except TypeError:
            # Support for old-style process_form methods
            result = field.widget.process_form(self, field, form,
                                               empty_marker=_marker)

        # Set things by calling the mutator
        mutator = field.getMutator(self)
        __traceback_info__ = (self, field, mutator)
        result[1]['field'] = field.__name__
        mapply(mutator, result[0], **result[1])

        self.reindexObject()
        self.at_post_edit_script()
        event.notify(objectevent.ObjectModifiedEvent(self))

        logging.info("SimpleProcessForm done")
        return

    security.declareProtected(permissions.View, 'simple_validate')
    def simple_validate(self, REQUEST, errors=None):

        #customized because we don't want to validate a whole
        #schemata, because some fields are required

        if errors is None:
            errors = {}

        _marker = []
        form = REQUEST.form
        instance = self

        fieldname = None
        for name in form.keys():
            if name in self.schema.keys():
                fieldname = name
                break
        if not fieldname:
            raise ValueError("Could not get valid field from the request")

        fields = [(field.getName(), field) for field in
                        self.schema.filterFields(__name__=fieldname)]
        for name, field in fields:
            error = 0
            value = None
            widget = field.widget
            if form:
                result = widget.process_form(instance, field, form,
                                             empty_marker=_marker)
            else:
                result = None
            if result is None or result is _marker:
                accessor = field.getEditAccessor(instance) or field.getAccessor(instance)
                if accessor is not None:
                    value = accessor()
                else:
                    # can't get value to validate -- bail
                    continue
            else:
                value = result[0]

            res = field.validate(instance=instance,
                                 value=value,
                                 errors=errors,
                                 REQUEST=REQUEST)
            if res:
                errors[field.getName()] = res
        return errors



registerType(Specification, PROJECTNAME)
# end of class Specification

##code-section module-footer #fill in your manual code here
class SpecificationFactories(object):
    """A simple class that provides some inteligence for specification object factories"""

    def __init__(self, spec):
        self.spec = spec

    def __getitem__(self, name):
        return getattr(self, 'factory_' + name)

    def factory_RationaleReference(self):
        type_name = 'RationaleReference'
        id = self.spec.generateUniqueId(type_name)
        new_id = self.spec.invokeFactory(type_name=type_name,
                id=id,
                title=_("Newly created Rationale Reference"))
        ref = self.spec[new_id]
        return ref

    def factory_PolicyQuestion(self):
        type_name = 'PolicyQuestion'
        id = self.spec.generateUniqueId(type_name)
        new_id = self.spec.invokeFactory(type_name=type_name,
                id=id,
                title=_("Newly created Policy Question"))
        ref = self.spec[new_id]
        return ref

##/code-section module-footer



