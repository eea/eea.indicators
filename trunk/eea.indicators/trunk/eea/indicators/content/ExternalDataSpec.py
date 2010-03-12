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
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema

##code-section module-header #fill in your manual code here
from Products.CMFPlone.utils import getToolByName
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Dataset name",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
        searchable=True,
    ),
    StringField(
        name='provider_name',
        required_for_publication="True",
        widget=StringField._properties['widget'](
            label="Dataset provider name",
            label_msgid='indicators_label_provider_name',
            i18n_domain='indicators',
        ),
        required=True,
        searchable=True,
    ),
    StringField(
        name='provider_url',
        required_for_publication="True",
        widget=StringField._properties['widget'](
            label="Provider URL",
            label_msgid='indicators_label_provider_url',
            i18n_domain='indicators',
        ),
        required=True,
    ),
    StringField(
        name='dataset_url',
        required_for_publication="True",
        widget=StringField._properties['widget'](
            label="Dataset URL",
            label_msgid='indicators_label_dataset_url',
            i18n_domain='indicators',
        ),
        required=True,
    ),
    TextField(
        name='dataset_path',
        widget=TextAreaWidget(
            label="Dataset path",
            label_msgid='indicators_label_dataset_path',
            i18n_domain='indicators',
        ),
        required=True,
    ),
    TextField(
        name='timelines',
        widget=TextAreaWidget(
            label="Timelines",
            label_msgid='indicators_label_timelines',
            i18n_domain='indicators',
        ),
        required=False,
        searchable=True,
    ),
    TextField(
        name='other_comments',
        widget=TextAreaWidget(
            label="Other Comments",
            label_msgid='indicators_label_other_comments',
            i18n_domain='indicators',
        ),
        required=False,
        searchable=True,
    ),
    StringField(
        name='category_of_use',
        widget=SelectionWidget(
            label="Category of use",
            label_msgid='indicators_label_category_of_use',
            i18n_domain='indicators',
        ),
        required=False,
        vocabulary= [['DataUseCategory_01','Main dataset'],['DataUseCategory_02','Dataset for gapfilling'],['DataUseCategory_03','Dataset for normalizing'],['DataUseCategory_04','Indicator dataset']],
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        required_for_publication="True",
        widget=RichWidget(
            label="Entities description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        required=True,
        searchable=True,
        default_output_type='text/html',
        accessor="getDescription",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
ExternalDataSpec_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

finalizeATCTSchema(ExternalDataSpec_schema)
##/code-section after-local-schema

ExternalDataSpec_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ExternalDataSpec(ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IExternalDataSpec)

    meta_type = 'ExternalDataSpec'
    _at_rename_after_creation = True

    schema = ExternalDataSpec_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDescription()).getData()



registerType(ExternalDataSpec, PROJECTNAME)
# end of class ExternalDataSpec

##code-section module-footer #fill in your manual code here
##/code-section module-footer



