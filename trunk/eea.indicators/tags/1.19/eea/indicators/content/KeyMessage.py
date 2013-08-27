# -*- coding: utf-8 -*-
#
# $Id$
#

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema
from Products.Archetypes.atapi import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from eea.indicators.config import *
from zope.interface import implements
import interfaces

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

KeyMessage_schema = ATContentTypeSchema.copy() + \
    schema.copy()

KeyMessage_schema['title'].required = False
KeyMessage_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}

class KeyMessage(ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IKeyMessage)

    meta_type = 'KeyMessage'
    _at_rename_after_creation = True

    schema = KeyMessage_schema

    security.declarePublic("Title")
    def Title(self):
        return self.getId()


registerType(KeyMessage, PROJECTNAME)