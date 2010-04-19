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
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema

##code-section module-header #fill in your manual code here
from Products.CMFPlone.utils import getToolByName
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from eea.indicators import msg_factory as _
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        searchable=False,
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Description',
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),
    TextField(
        name='needs',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Needs',
            label_msgid='indicators_label_needs',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
    ),
    StringField(
        name='status',
        widget=SelectionWidget(
            label='Status',
            label_msgid='indicators_label_status',
            i18n_domain='indicators',
        ),
        required=True,
        vocabulary=["Not started", "In progress", "Completed"],
    ),
    DateTimeField(
        name='due_date',
        widget=DateTimeField._properties['widget'](
            label="Due date",
            label_msgid='indicators_label_due_date',
            i18n_domain='indicators',
        ),
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

WorkItem_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
finalizeATCTSchema(WorkItem_schema)
WorkItem_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class WorkItem(ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IWorkItem)

    meta_type = 'WorkItem'
    _at_rename_after_creation = True

    schema = WorkItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        if not(self.getDue_date()):
            return _(
                    "title-work-get-title-none",
                    default="Newly created work item"
                    )

        duedate = self.toLocalizedTime(self.getDue_date(), long_format=0)
        title = _("work-work-aggregated",
                default="Work ${status} due ${due}",
                mapping = {
                    'status':self.getStatus(),
                    'due':duedate,
                    }
                )
        return self.translate(title)

    security.declarePublic("Description")
    def Description(self):
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDescription()).getData()



registerType(WorkItem, PROJECTNAME)
# end of class WorkItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



