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
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        accessor="Title",
    ),
    StringField(
        name='link',
        widget=StringField._properties['widget'](
            label='Link',
            label_msgid='indicators_label_link',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        accessor="Description",
    ),
    StringField(
        name='reference_type',
        widget=SelectionWidget(
            label="Reference type",
            label_msgid='indicators_label_reference_type',
            i18n_domain='indicators',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RationaleReference_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RationaleReference(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IRationaleReference)

    meta_type = 'RationaleReference'
    _at_rename_after_creation = True

    schema = RationaleReference_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(RationaleReference, PROJECTNAME)
# end of class RationaleReference

##code-section module-footer #fill in your manual code here
##/code-section module-footer



