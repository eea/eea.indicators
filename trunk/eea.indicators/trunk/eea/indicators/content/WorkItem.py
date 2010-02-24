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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

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
        widget=TextAreaWidget(
            label_msgid="IMS_workitem_description_label",
            label='Description',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='needs',
        widget=TextAreaWidget(
            label_msgid="IMS_workitem_needs_label",
            label='Needs',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='status',
        widget=SelectionWidget(
            label_msgid="IMS_workitem_status_label",
            label='Status',
            i18n_domain='indicators',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

WorkItem_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class WorkItem(BaseContent, BrowserDefaultMixin):
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


registerType(WorkItem, PROJECTNAME)
# end of class WorkItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



