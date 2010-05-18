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

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from eea.indicators.content.interfaces import ISpecification
from eea.indicators.content.utils import get_specific_parent
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
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

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AssessmentPart_schema = ATFolderSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
AssessmentPart_schema.moveField('relatedItems', pos=0)
AssessmentPart_schema['relatedItems'] = EEAReferenceField('relatedItems',
        relationship='relatesTo',
        required=True,
        multiValued=False,
        validators=('one_assessment_per_question',),
        widget=EEAReferenceBrowserWidget(
            label="Answers to policy question",
            label_msgid='indicators_label_question_answered',
            i18n_domain='indicators',
            ))
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
            q = self.getRelatedItems()
        except AttributeError:  #reference_catalog is not found at creation
            q = None
        if not q:
            return "Answer to unknown question"

        #return u"Answer for: %s" % q.Title()
        return q[0].Title()

    security.declarePublic('is_key_message')
    def is_key_message(self):
        q = self.getRelatedItems()
        if not q:
            return False
        return q[0].getIs_key_question()

    security.declarePublic('get_specification_path')
    def get_specification_path(self):
        #returns the path to the specification, used by the ReferenceWidget
        spec = self.aq_parent.aq_parent #Specification -> Assessment -> AssessmentPart
        return spec.getPhysicalPath()

    def factory_EEAFigure(self):
        type_name = 'EEAFigure'
        figure = self._generic_factory(type_name)

        try:
            spec = get_specific_parent(self, lambda o:ISpecification.providedBy(o))
            themes = spec.getThemes()
        except ValueError:
            themes = []

        figure.setThemes(themes)
        return {'obj':figure, 'subview':'edit', 'direct_edit':True}



registerType(AssessmentPart, PROJECTNAME)
# end of class AssessmentPart

##code-section module-footer #fill in your manual code here
##/code-section module-footer



