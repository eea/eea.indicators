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
from Products.ATContentTypes.content.file import ATFile
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.file import ATFile, ATFileSchema

##code-section module-header #fill in your manual code here
from eea.dataservice.fields import EventFileField
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        required_for_published=True,
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
    ),
    TextField(
        name='description',
        required_for_published=True,
        widget=TextAreaWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        description="True",
        searchable=True,
        required=True,
        accessor="getDescription",
    ),
    EventFileField('file',
        required=False,
        primary=True,
        widget = FileWidget(
            description = "Select the file to be added by clicking the 'Browse' button.",
            description_msgid = "help_file",
            label= "File",
            label_msgid = "label_file",
            i18n_domain = "plone",
            show_content_type = False,)),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FactSheetDocument_schema = ATFileSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
FactSheetDocument_schema['description'].required = False
FactSheetDocument_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class FactSheetDocument(ATFile, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IFactSheetDocument)

    meta_type = 'FactSheetDocument'
    _at_rename_after_creation = True

    schema = FactSheetDocument_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(FactSheetDocument, PROJECTNAME)
# end of class FactSheetDocument

##code-section module-footer #fill in your manual code here
##/code-section module-footer
