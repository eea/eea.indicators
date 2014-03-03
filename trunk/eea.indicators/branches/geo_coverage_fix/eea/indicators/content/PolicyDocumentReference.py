# -*- coding: utf-8 -*-
#
# $Id$
#
""" Policy Document Reference
"""
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.content.link import ATLink
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import Schema, StringField
from Products.Archetypes.atapi import TextField, RichWidget
from Products.CMFCore import permissions
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import getToolByName
from eea.themecentre.content.ThemeTaggable import ThemeTaggable
from eea.themecentre.content.ThemeTaggable import ThemeTaggable_schema
from eea.indicators.content import  interfaces
from zope.interface import implements
import logging

logger = logging.getLogger('eea.indicators.content.PolicyDocumentReference')

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
        validators=('unique_policy_title_validator',),
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        allowable_content_types=('text/plain', 'text/structured',
                                 'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),
    StringField(
        name='remoteUrl',
        widget=StringField._properties['widget'](
            label='Remoteurl',
            label_msgid='indicators_label_remoteUrl',
            i18n_domain='indicators',
        ),
        searchable=True,
        validators=('isURL', 'unique_policy_url_validator'),
        default="http://",
        required=True,
        primary=True,
    ),

),
)


PolicyDocumentReference_schema = (
    ATContentTypeSchema.copy() +
    ThemeTaggable_schema.copy() +
    getattr(ATLink, 'schema', Schema(())).copy() +
    schema.copy()
)

finalizeATCTSchema(PolicyDocumentReference_schema)
PolicyDocumentReference_schema['relatedItems'].widget.visible = {
    'view':'invisible',
    'edit':'invisible',
}

class PolicyDocumentReference(ATCTContent, ATLink,
                              BrowserDefaultMixin, ThemeTaggable):
    """PolicyDocumentReference content class
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPolicyDocumentReference)

    meta_type = 'PolicyDocumentReference'
    _at_rename_after_creation = True

    schema = PolicyDocumentReference_schema

    security.declarePublic("Description")
    def Description(self):
        """Description"""
        convert = getToolByName(self, 'portal_transforms').convert
        text = convert('html_to_text', self.getDescription()).getData()
        try:
            text = text.decode('utf-8', 'replace')
        except UnicodeDecodeError, err:
            logger.info(err)
        return text

    security.declareProtected(permissions.View, 'getUrl')
    def getUrl(self):
        """ getUrl"""
        field = self.getField('remoteUrl')
        return field.getAccessor(self)()
