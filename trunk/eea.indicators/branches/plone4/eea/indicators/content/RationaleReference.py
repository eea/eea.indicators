# -*- coding: utf-8 -*-
#
# $Id$
#

"""RationaleReference content type
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.link import ATLink, ATLinkSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import Schema, StringField, registerType
from Products.Archetypes.atapi import TextField, RichWidget, SelectionWidget
from Products.CMFCore import permissions
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import getToolByName
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from zope.interface import implements
import logging

logger = logging.getLogger('eea.indicators.content.RationaleReference')

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
    StringField(
        name='reference_type',
        widget=SelectionWidget(
            label="Reference type",
            format="select",
            label_msgid='indicators_label_reference_type',
            i18n_domain='indicators',
        ),
        required=True,
        vocabulary=[("",""), ("RationaleRefType_01", "Scientific reference"), 
            ("RationaleRefType_02", "Reference to other indicator initiative") ],
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
        searchable=True,
        required_for_published=True,
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 
                                 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),

),
)

RationaleReference_schema = ATLinkSchema.copy() + \
    getattr(ATLink, 'schema', Schema(())).copy() + \
    schema.copy()

RationaleReference_schema['relatedItems'].widget.visible = {'view':'invisible', 
                                                            'edit':'invisible'}
finalizeATCTSchema(RationaleReference_schema)

class RationaleReference(ATLink, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IRationaleReference)

    meta_type = 'RationaleReference'
    _at_rename_after_creation = True

    schema = RationaleReference_schema


    security.declarePublic("Description")
    def Description(self):
        """Returns description"""
        convert = getToolByName(self, 'portal_transforms').convert
        text = convert('html_to_text', self.getDescription()).getData()
        try:
            text = text.decode('utf-8', 'replace')
        except UnicodeDecodeError, err:
            logger.info(err)
        return text

    security.declareProtected(permissions.View, 'getUrl')
    def getUrl(self):
        """ """
        field = self.getField('remoteUrl')
        return field.getAccessor(self)()


registerType(RationaleReference, PROJECTNAME)
