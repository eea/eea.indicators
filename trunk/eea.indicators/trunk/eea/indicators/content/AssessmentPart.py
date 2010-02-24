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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from eea.indicators.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    TextField(
        name='assessment',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Assessment',
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
    ),
    ReferenceField(
        name='policyquestions',
        widget=ReferenceBrowserWidget(
            label='Policyquestions',
            label_msgid='indicators_label_policyquestions',
            i18n_domain='indicators',
        ),
        allowed_types=('PolicyQuestion',),
        multiValued=0,
        relationship='answers_to_question',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AssessmentPart_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class AssessmentPart(BaseFolder, BrowserDefaultMixin):
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


registerType(AssessmentPart, PROJECTNAME)
# end of class AssessmentPart

##code-section module-footer #fill in your manual code here
##/code-section module-footer



