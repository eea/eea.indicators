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

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Question",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
    ),
    BooleanField(
        name='is_key_question',
        widget=BooleanField._properties['widget'](
            label="Is this a key question?",
            label_msgid='indicators_label_is_key_question',
            i18n_domain='indicators',
        ),
    ),
    ReferenceField(
        name='eeafigures',
        widget=ReferenceBrowserWidget(
            label="Example EEA Figure",
            label_msgid='indicators_label_eeafigures',
            i18n_domain='indicators',
        ),
        allowed_types=('EEAFigure',),
        multiValued=0,
        relationship='example_figure',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PolicyQuestion_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PolicyQuestion(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPolicyQuestion)

    meta_type = 'PolicyQuestion'
    _at_rename_after_creation = True

    schema = PolicyQuestion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(PolicyQuestion, PROJECTNAME)
# end of class PolicyQuestion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



