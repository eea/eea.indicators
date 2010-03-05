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
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='due_date',
        widget=DateTimeField._properties['widget'](
            label="Due date",
            label_msgid="IMS_workitem_duedate_label",
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label_msgid="IMS_workitem_description_label",
            label='Description',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        accessor="Description",
    ),
    TextField(
        name='needs',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label_msgid="IMS_workitem_needs_label",
            label='Needs',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
    ),
    StringField(
        name='status',
        widget=SelectionWidget(
            label_msgid="IMS_workitem_status_label",
            label='Status',
            i18n_domain='indicators',
        ),
        vocabulary= ["Not started", "In progress", "Completed" ],
    ),
    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible={'view':'hidden', 'edit':'hidden'},
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=False,
        accessor="Title",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

WorkItem_schema = ATFolderSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class WorkItem(ATFolder, ATCTContent, BrowserDefaultMixin):
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

    security.declarePublic('getTitle')
    def getTitle(self):
        return "Work in progress due %s" % self.getDue_date()



registerType(WorkItem, PROJECTNAME)
# end of class WorkItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



