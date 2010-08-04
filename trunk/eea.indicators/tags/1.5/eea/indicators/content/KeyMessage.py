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
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    TextField(
        name='message',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        required_for_published=True,
        widget=RichWidget(
            label="Key message",
            label_msgid='indicators_label_message',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        searchable=True,
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

KeyMessage_schema = ATContentTypeSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
KeyMessage_schema['title'].required = False
KeyMessage_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class KeyMessage(ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IKeyMessage)

    meta_type = 'KeyMessage'
    _at_rename_after_creation = True

    schema = KeyMessage_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic("Title")
    def Title(self):
        return self.getId()


registerType(KeyMessage, PROJECTNAME)
# end of class KeyMessage

##code-section module-footer #fill in your manual code here
##/code-section module-footer



