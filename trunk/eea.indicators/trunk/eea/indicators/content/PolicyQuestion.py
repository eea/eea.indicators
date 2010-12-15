# -*- coding: utf-8 -*-
#
# $Id$
#

"""Policy Question content class
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import BooleanField, registerType, TextAreaWidget
from Products.Archetypes.atapi import Schema, StringField, TextField
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from zope.interface import implements

schema = Schema((

    StringField(
        name='title',
        required_for_published=True,
        widget=StringField._properties['widget'](
            label="Question",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
        searchable=True,
    ),
    BooleanField(
        name='is_key_question',
        widget=BooleanField._properties['widget'](
            label="Is this a key question?",
            label_msgid='indicators_label_is_key_question',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            visible={'view':'invisible', 'edit':'invisible'},
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        accessor="Description",
        searchable=True,
    ),

),
)

PolicyQuestion_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

finalizeATCTSchema(PolicyQuestion_schema)
PolicyQuestion_schema['relatedItems'].widget.visible = {'view':'invisible', 
                                                        'edit':'invisible'}

class PolicyQuestion(ATCTContent, BrowserDefaultMixin):
    """ Policy Question content type
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPolicyQuestion)

    meta_type = 'PolicyQuestion'
    _at_rename_after_creation = True

    schema = PolicyQuestion_schema


registerType(PolicyQuestion, PROJECTNAME)
