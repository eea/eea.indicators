# -*- coding: utf-8 -*-
#
# $Id$
#
""" Assessment Part
"""

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent, aq_base
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import Schema, RichWidget
from Products.Archetypes.atapi import TextField, StringField, TextAreaWidget
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from eea.indicators.content import  interfaces
from eea.indicators.content.base import CustomizedObjectFactory
from eea.indicators.content.base import ModalFieldEditableAware
from eea.indicators.content.interfaces import ISpecification
from eea.indicators.content.utils import get_specific_parent
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
from plone.uuid.interfaces import IUUID
from zope.interface import implements


schema = Schema((

    TextField(
        name='assessment',
        widget=RichWidget(
            label='Assessment',
            description='Assessment',
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
            ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured',
             'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        ),
    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
            label='Title',
            description='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
            ),
        required=False,
        accessor="Title",
        ),
    TextField(
        name='description',
        default="",
        widget=TextAreaWidget(
            visible={'edit' : 'invisible', 'view' : 'invisible' },
            label='Description',
            description='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
            ),
        accessor="Description",
        searchable=True,
        ),
    EEAReferenceField(
        name="relatedItems",
        multiValued=True,
        relationship='relatesTo',
        required=True,
        validators=('one_assessment_per_question',),
        #referencesSortable=True,
        keepReferencesOnCopy=True,
        accessor="get_related_items",
        edit_accessor="get_raw_related_items",
        mutator="set_related_items",
        widget=EEAReferenceBrowserWidget(
            label="Answers to policy question and related EEAFigures",
            description='Answers to policy question and related EEAFigures',
            label_msgid='indicators_label_question_answered',
            i18n_domain='indicators',
            macro="assessmentpart_relationwidget",
            )
        ),
    ),
)

AssessmentPart_schema = ATFolderSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

AssessmentPart_schema.moveField('relatedItems', pos=0)
finalizeATCTSchema(AssessmentPart_schema)

class AssessmentPart(ATFolder, ModalFieldEditableAware,
        CustomizedObjectFactory, ATCTContent, BrowserDefaultMixin):
    """Assessment part
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAssessmentPart)

    meta_type = 'AssessmentPart'
    _at_rename_after_creation = False

    schema = AssessmentPart_schema

    security.declareProtected("View", "index_html")
    def index_html(self):
        """Redirect to parent"""
        url = aq_parent(aq_inner(self)).absolute_url()
        return self.REQUEST.response.redirect(url)

    def get_related_question(self):
        """Get related q"""
        question = None
        try:
            relations = self.getRelatedItems()
        except AttributeError:
            relations = [] #reference_catalog is not found at creation
        for ob in relations:
            if ob is not None:
                if ob.portal_type == 'PolicyQuestion':
                    question = ob
                    break
        return question

    security.declarePublic('Title')
    def Title(self):
        """Title"""
        question = self.get_related_question()

        if question:
            return question.Title().encode('utf-8')
        else:
            return "Answer to unknown question"

    security.declarePublic('is_key_message')
    def is_key_message(self):
        """ is key message?"""
        question = self.get_related_question()

        if question:
            return question.getIs_key_question()
        else:
            return False

    security.declarePublic('get_specification_path')
    def get_specification_path(self):
        """get spec path"""
        #returns the path to the specification, used by the ReferenceWidget
        #Specification -> Assessment -> AssessmentPart
        spec = aq_parent(aq_inner(self))
        return spec.getPhysicalPath()

    def factory_EEAFigure(self):
        """Factory for eea figures"""
        #ZZZ: is this used anymore?
        type_name = 'EEAFigure'
        info = self._generic_factory(type_name)
        figure = info['obj']

        try:
            spec = get_specific_parent(self,
                                      lambda o:ISpecification.providedBy(o))
            themes = spec.getThemes()
        except ValueError:
            themes = []

        figure.setThemes(themes)
        return {'obj':figure, 'subview':'edit', 'direct_edit':True}

    security.declareProtected('View', 'get_related_items')
    def get_related_items(self):
        """ Related items
        """
        field = self.getField('relatedItems')
        res = self.getRefs(relationship=field.relationship)
        rd = {}
        for r in res:
            rd.__setitem__(IUUID(r, None), r)

        #not field.referencesSortable or
        if not hasattr(aq_base(self), 'at_ordered_refs'):
            return res

        refs = self.at_ordered_refs
        order = refs.get(field.relationship)
        if not order:
            return res

        res = [rd[uid] for uid in order if uid in rd.keys()]
        return res

    #security.declareProtected('View', 'get_raw_related_items')
    def get_raw_related_items(self):
        """ Raw related items
        """
        instance = self
        field = self.getField('relatedItems')

        rc = getToolByName(instance, REFERENCE_CATALOG)
        brains = rc(sourceUID=IUUID(instance, None),
                    relationship=field.relationship)
        res = [b.targetUID for b in brains]
        if not field.multiValued: #and not aslist:
            if res:
                res = res[0]
            else:
                res = None

        if not hasattr(aq_base(instance), 'at_ordered_refs'):
            return res

        refs = instance.at_ordered_refs
        order = refs.get(field.relationship)
        if not order:
            return res
        res = [r for r in order if r in res]

        return res

    security.declareProtected('View', 'getRelatedItems')
    def getRelatedItems(self):
        """ Related items
        """
        return self.get_related_items()

    security.declareProtected('Modify portal content', 'set_related_items')
    def set_related_items(self, value):
        """ Set related items
        """
        #import pdb; pdb.set_trace()
        instance = self
        field = self.getField('relatedItems')

        tool = getToolByName(instance, REFERENCE_CATALOG)
        targetUIDs = [ref.targetUID for ref in
                      tool.getReferences(instance, field.relationship)]

        if value is None:
            value = ()

        if not isinstance(value, (list, tuple)):
            value = value,
        elif not field.multiValued and len(value) > 1:
            raise ValueError, \
                  "Multiple values given for single valued field %r" % self

        #convert objects to uids if necessary
        uids = []
        for v in value:
            if isinstance(v, basestring):
                uids.append(v)
            else:
                uids.append(IUUID(v, None))

        add = [x for x in uids if x and x not in targetUIDs]
        sub = [t for t in targetUIDs if t not in uids]

        for uid in add:
            #__traceback_info__ = (instance, uid, value, targetUIDs)
            # throws IndexError if uid is invalid
            tool.addReference(instance, uid, field.relationship)

        for uid in sub:
            tool.deleteReference(instance, uid, field.relationship)

        if not hasattr( aq_base(instance), 'at_ordered_refs'):
            instance.at_ordered_refs = {}

        uids = tuple([u for u in uids if u is not None])
        instance.at_ordered_refs[field.relationship] = uids

