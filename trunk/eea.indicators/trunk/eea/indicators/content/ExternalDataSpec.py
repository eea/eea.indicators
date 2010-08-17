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
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary

##code-section module-header #fill in your manual code here
from Products.CMFPlone.utils import getToolByName
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from eea.dataservice.vocabulary import Organisations
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
        widget=StringField._properties['widget'](
            visible={'view':'visible', 'edit':'visible'},
            label="Dataset provider name",
            label_msgid='indicators_label_provider_name',
            i18n_domain='indicators',
        ),
        required=False,
        searchable=True,
    ),
    StringField(
        name='provider_url',
        widget=SelectionWidget(
            label="Dataset provider",
            description="Organisation providing access to this dataset.",
            macro="organisation_widget",
            helper_js=("selectautocomplete_widget.js", ),
            label_msgid='indicators_label_provider_url',
            i18n_domain='indicators',
        ),
        required=True,
        required_for_published="True",
        vocabulary=Organisations(),
    ),
    StringField(
        name='dataset_url',
        widget=SelectionWidget(
            label="Dataset URL",
            macro="organisation_widget",
            helper_js=("selectautocomplete_widget.js", ),
            label_msgid='indicators_label_dataset_url',
            i18n_domain='indicators',
        ),
        required=True,
        required_for_published="False",
        vocabulary=Organisations(),
    ),
    StringField(
        name='data_url',
        widget=StringField._properties['widget'](
            visible={'view':'hidden', 'edit':'visible'},
            label="URL where this dataset can be found",
            label_msgid='indicators_label_data_url',
            i18n_domain='indicators',
        ),
        required=True,
        searchable=True,
        required_for_published="True",
    ),
    TextField(
        name='dataset_path',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Dataset path",
            description="Further information and details needed to get the dataset.",
            label_msgid='indicators_label_dataset_path',
            i18n_domain='indicators',
        ),
        required=True,
        default_content_type="text/html",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='timeliness',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Timelines",
            label_msgid='indicators_label_timeliness',
            i18n_domain='indicators',
        ),
        required=False,
        default_content_type="text/html",
        searchable=True,
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='other_comments',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Other Comments",
            label_msgid='indicators_label_other_comments',
            i18n_domain='indicators',
        ),
        required=False,
        default_content_type="text/html",
        searchable=True,
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='category_of_use',
        widget=SelectionWidget(
            label="Category of use",
            label_msgid='indicators_label_category_of_use',
            i18n_domain='indicators',
        ),
        required=False,
        vocabulary=NamedVocabulary("indicator_category_of_use"),
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label="Entities description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        required_for_published="True",
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
schema['provider_url'].validators=('isURL',)
schema['dataset_url'].validators=('isURL',)
schema['data_url'].validators=('isURL',)
##/code-section after-local-schema

ExternalDataSpec_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
ExternalDataSpec_schema.moveField('relatedItems', after='category_of_use')
finalizeATCTSchema(ExternalDataSpec_schema)
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



