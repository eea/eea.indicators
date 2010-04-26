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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from eea.indicators.content.base import ModalFieldEditableAware, CustomizedObjectFactory
##/code-section module-header

schema = Schema((

    TextField(
        name='assessment',
        widget=RichWidget(
            label='Assessment',
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
            label='Title',
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
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        accessor="Description",
        searchable=True,
    ),
    ReferenceField(
        name='question_answered',
        widget=ReferenceBrowserWidget(
            label="Answers to policy question",
            label_msgid='indicators_label_question_answered',
            i18n_domain='indicators',
        ),
        relationship='relates_to',
        required=True,
        multiValued=0,
        validators=('one_assessment_per_question',),
        allowed_types=('PolicyQuestion',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AssessmentPart_schema = ATFolderSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
AssessmentPart_schema['question_answered'].widget = ReferenceWidget(
            label="Answers to policy question",
            label_msgid='indicators_label_question_answered',
            i18n_domain='indicators',
            destination="get_specification_path",
        )
AssessmentPart_schema.moveField('question_answered', pos=0)
AssessmentPart_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
finalizeATCTSchema(AssessmentPart_schema)
##/code-section after-schema

class AssessmentPart(ATFolder, ModalFieldEditableAware,  CustomizedObjectFactory, ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAssessmentPart)

    meta_type = 'AssessmentPart'
    _at_rename_after_creation = True

    schema = AssessmentPart_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        try:
            q = self.getQuestion_answered()
        except AttributeError:  #reference_catalog is not found at creation
            q = None
        if q is None:
            return "Answer to unknown question"
        #return u"Answer for: %s" % q.Title()
        return q.Title()

    security.declarePublic('is_key_message')
    def is_key_message(self):
        q = self.getQuestion_answered()
        if q is None:
            return False
        return q.getIs_key_question()

    security.declarePublic('get_specification_path')
    def get_specification_path(self):
        #returns the path to the specification, used by the ReferenceWidget
        spec = self.aq_parent.aq_parent #Specification -> Assessment -> AssessmentPart
        return spec.getPhysicalPath()

    def factory_EEAFigure(self):
        type_name = 'EEAFigure'
        return self._generic_factory(type_name)



registerType(AssessmentPart, PROJECTNAME)
# end of class AssessmentPart

##code-section module-footer #fill in your manual code here
##/code-section module-footer



