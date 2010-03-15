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
##/code-section module-header

schema = Schema((

    TextField(
        name='assessment',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        required_for_publication=True,
        widget=RichWidget(
            label='Assessment',
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
        ),
        required=True,
        searchable=True,
        default_output_type='text/html',
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
        allowed_types=('PolicyQuestion',),
        multiValued=0,
        relationship='relates_to',
        required=True,
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
finalizeATCTSchema(AssessmentPart_schema)
##/code-section after-schema

class AssessmentPart(ATFolder, ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAssessmentPart)

    meta_type = 'AssessmentPart'
    _at_rename_after_creation = False

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
        import pdb; pdb.set_trace()
        spec = self.aq_parent.aq_parent #Specification -> Assessment -> AssessmentPart
        return spec.getPhysicalPath()



registerType(AssessmentPart, PROJECTNAME)
# end of class AssessmentPart

##code-section module-footer #fill in your manual code here
##/code-section module-footer



