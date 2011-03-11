# -*- coding: utf-8 -*-
#
# $Id$

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import RichWidget, registerType, DateTimeField
from Products.Archetypes.atapi import Schema, TextField, StringField
from Products.Archetypes.atapi import SelectionWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import getToolByName
from eea.indicators import msg_factory as _
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from zope.interface import implements
import logging

logger = logging.getLogger('eea.indicators.content.WorkItem')

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
        allowable_content_types=('text/plain', 'text/structured', 
             'text/html', 'application/msword',),
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
        allowable_content_types=('text/plain', 'text/structured', 
            'text/html', 'application/msword',),
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


WorkItem_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

finalizeATCTSchema(WorkItem_schema)
WorkItem_schema['relatedItems'].widget.visible = {'view':'invisible', 
                                                  'edit':'invisible'}

class WorkItem(ATCTContent, BrowserDefaultMixin):
    """WorkItem content class
    """
    security = ClassSecurityInfo()

    implements(interfaces.IWorkItem)

    meta_type = 'WorkItem'
    _at_rename_after_creation = True

    schema = WorkItem_schema

    security.declarePublic('Title')
    def Title(self):
        """title"""
        if not(self.getDue_date()):
            return _(
                    "title-work-get-title-none",
                    default="Newly created work item"
                    )

        duedate = self.toLocalizedTime(self.getDue_date(), long_format=0)
        title = _("work-work-aggregated",
                default="Work due ${due}",  #${status} 
                mapping = {
                    #'status':self.getStatus(),
                    'due':duedate,
                    }
                )
        return self.translate(title)

    security.declarePublic("Description")
    def Description(self):
        """Description"""
        convert = getToolByName(self, 'portal_transforms').convert
        text = convert('html_to_text', self.getDescription()).getData()
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError, err:
            logger.info(err)
        return text


registerType(WorkItem, PROJECTNAME)
