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
    ),
    StringField(
        name='provider_name',
        widget=StringField._properties['widget'](
            label="Dataset provider name",
            label_msgid='indicators_label_provider_name',
            i18n_domain='indicators',
        ),
        required=True,
    ),
    StringField(
        name='provider_url',
        widget=StringField._properties['widget'](
            label="Provider URL",
            label_msgid='indicators_label_provider_url',
            i18n_domain='indicators',
        ),
        required=True,
    ),
    StringField(
        name='dataset_url',
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
        required=True,
    ),
    TextField(
        name='other_comments',
        widget=TextAreaWidget(
            label="Other Comments",
            label_msgid='indicators_label_other_comments',
            i18n_domain='indicators',
        ),
        required=False,
    ),
    StringField(
        name='category_of_use',
        widget=SelectionWidget(
            label="Category of use",
            label_msgid='indicators_label_category_of_use',
            i18n_domain='indicators',
        ),
        required=True,
        vocabulary= [['DataUseCategory_01','Main dataset'],['DataUseCategory_02','Dataset for gapfilling'],['DataUseCategory_03','Dataset for normalizing'],['DataUseCategory_04','Indicator dataset']],
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Entities description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        accessor="Description",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ExternalDataSpec_schema = ATFolderSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ExternalDataSpec(ATFolder, ATCTContent, BrowserDefaultMixin):
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


registerType(ExternalDataSpec, PROJECTNAME)
# end of class ExternalDataSpec

##code-section module-footer #fill in your manual code here
##/code-section module-footer



