# -*- coding: utf-8 -*-
#
# $Id$

"""Methodology Reference content type
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.link import ATLink, ATLinkSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import StringField, Schema, TextField
from Products.Archetypes.atapi import registerType, RichWidget
from Products.CMFCore import permissions
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import getToolByName
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from zope.interface import implements
import logging

logger = logging.getLogger('eea.indicators.content.MethodologyReference')


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
        required_for_published=True,
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        description="True",
        searchable=True,
        required=True,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 
                                 'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),

),
)

MethodologyReference_schema = ATLinkSchema.copy() + \
    getattr(ATLink, 'schema', Schema(())).copy() + \
    schema.copy()

MethodologyReference_schema['relatedItems'].widget.visible = {'view':'invisible',  
                                                              'edit':'invisible'}
finalizeATCTSchema(MethodologyReference_schema)

class MethodologyReference(ATLink, BrowserDefaultMixin):
    """MethodologyReference content class
    """
    security = ClassSecurityInfo()

    implements(interfaces.IMethodologyReference)

    meta_type = 'MethodologyReference'
    _at_rename_after_creation = True

    schema = MethodologyReference_schema

    security.declarePublic("Description")
    def Description(self):
        """Returns description"""
        convert = getToolByName(self, 'portal_transforms').convert
        text = convert('html_to_text', self.getDescription()).getData()
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError, err:
            logger.info(err)
        return text

    security.declareProtected(permissions.View, 'getUrl')
    def getUrl(self):
        """ returns url"""
        field = self.getField('remoteUrl')
        return field.getAccessor(self)()


registerType(MethodologyReference, PROJECTNAME)
