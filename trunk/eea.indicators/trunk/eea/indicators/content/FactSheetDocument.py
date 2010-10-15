# -*- coding: utf-8 -*-
#
# $Id$

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.file import ATFile, ATFileSchema
from Products.Archetypes.atapi import *
from Products.CMFCore.permissions import View
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from eea.dataservice.fields import EventFileField
from eea.indicators.config import *
from zope.interface import implements
import interfaces

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
    EventFileField('file',
        required=False,
        primary=True,
        widget = FileWidget(
            description = "Select the file to be added by clicking the 'Browse' button.",
            description_msgid = "help_file",
            label= "File",
            label_msgid = "label_file",
            i18n_domain = "plone",
            show_content_type = False,)),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FactSheetDocument_schema = ATFileSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
FactSheetDocument_schema['description'].required = False
FactSheetDocument_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class FactSheetDocument(ATFile, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IFactSheetDocument)

    meta_type = 'FactSheetDocument'
    _at_rename_after_creation = True

    schema = FactSheetDocument_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

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
# end of class FactSheetDocument

##code-section module-footer #fill in your manual code here
##/code-section module-footer
