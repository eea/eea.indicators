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

    TextField(
        name='key_message',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Key message",
            label_msgid='indicators_label_key_message',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
    ),
    IntegerField(
        name='mp_year',
        widget=IntegerField._properties['widget'](
            label="MP Year",
            label_msgid='indicators_label_mp_year',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='mp_code',
        widget=StringField._properties['widget'](
            label="MP Code",
            label_msgid='indicators_label_mp_code',
            i18n_domain='indicators',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Assessment_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Assessment(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAssessment)

    meta_type = 'Assessment'
    _at_rename_after_creation = True

    schema = Assessment_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('get_assessments')
    def get_assessments(self):
        parts = self.objectValues('AssessmentPart')
        key = None
        secondary = []
        for part in parts:
            if part.is_key_message():
                key = part
            else:
                secondary.append(part)

        return {
                'key':key,
                'secondary':secondary
                }


registerType(Assessment, PROJECTNAME)
# end of class Assessment

##code-section module-footer #fill in your manual code here
##/code-section module-footer



