# -*- coding: utf-8 -*-
#
# $Id$
#

"""KeyMessage content class
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.Archetypes.atapi import TextField, Schema
from Products.Archetypes.atapi import registerType, RichWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from eea.indicators.config import PROJECTNAME
from zope.interface import implements
from eea.indicators.content import interfaces

schema = Schema((

    TextField(
        name='message',
        allowable_content_types=('text/plain', 'text/structured', 
                      'text/html', 'application/msword',),
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
KeyMessage_schema['relatedItems'].widget.visible = {'view':'invisible', 
                                                    'edit':'invisible'}

class KeyMessage(ATCTContent, BrowserDefaultMixin):
    """KeyMessage content type
    """
    security = ClassSecurityInfo()

    implements(interfaces.IKeyMessage)

    meta_type = 'KeyMessage'
    _at_rename_after_creation = True

    schema = KeyMessage_schema

    security.declarePublic("Title")
    def Title(self):
        """Returns title"""
        return self.getId()


registerType(KeyMessage, PROJECTNAME)
