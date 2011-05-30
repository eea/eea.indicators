# -*- coding: utf-8 -*-
#
# $Id$

"""FactSheetDocument
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.file import ATFile, ATFileSchema
from Products.Archetypes.atapi import Schema, StringField
from Products.Archetypes.atapi import TextField, TextAreaWidget
from Products.Archetypes.atapi import registerType, FileWidget
from Products.CMFCore.permissions import View
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from plone.app.blob.field import BlobField
from zope.interface import implements

#from eea.dataservice.fields import EventFileField

schema = Schema((

    StringField(
        name='title',
        required_for_published=True,
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=True,
        accessor="Title",
    ),
    TextField(
        name='description',
        required_for_published=True,
        widget=TextAreaWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        description="True",
        searchable=True,
        required=True,
        accessor="getDescription",
    ),
    BlobField('file',
        required=False,
        primary=True,
        widget = FileWidget(
            description = "Select the file to be added by "
                          "clicking the 'Browse' button.",
            description_msgid = "help_file",
            label= "File",
            label_msgid = "label_file",
            i18n_domain = "plone",
            show_content_type = False,)),
),
)


FactSheetDocument_schema = ATFileSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

FactSheetDocument_schema['description'].required = False
FactSheetDocument_schema['relatedItems'].widget.visible = \
        {'view':'invisible', 'edit':'invisible'}

class FactSheetDocument(ATFile, BrowserDefaultMixin):
    """FactSheet Document
    """
    implements(interfaces.IFactSheetDocument)
    meta_type = 'FactSheetDocument'
    schema = FactSheetDocument_schema

    security = ClassSecurityInfo()
    _at_rename_after_creation = True

    security.declareProtected(View, 'index_html')
    def index_html(self, REQUEST=None, RESPONSE=None):
        """Make it directly viewable when entering the objects URL
        """
        #override index_html because it returns an recursion error #3533
        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE
        field = self.getPrimaryField()

        return field.index_html(self)   #this is what works

        #this is the original code
        #data  = field.getAccessor(self)(REQUEST=REQUEST, RESPONSE=RESPONSE)
        #if data:
        #    return data.index_html(REQUEST, RESPONSE)
        ## TODO what should be returned if no data is present?

registerType(FactSheetDocument, PROJECTNAME)
