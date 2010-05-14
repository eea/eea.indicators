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
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from eea.indicators.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from eea.dataservice.fields.ManagementPlanField import ManagementPlanField

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from eea.dataservice.vocabulary import DatasetYears
from eea.dataservice.widgets.ManagementPlanWidget import ManagementPlanWidget
from eea.indicators import msg_factory as _
from eea.indicators.content.base import ModalFieldEditableAware, CustomizedObjectFactory
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
##/code-section module-header

schema = Schema((

    TextField(
        name='key_message',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Key message",
            label_msgid='indicators_label_key_message',
            i18n_domain='indicators',
        ),
        default_content_type="text/html",
        searchable=True,
        default_output_type="text/x-html-safe",
        required_for_published=True,
    ),
    ManagementPlanField(
        name='management_plan',
        widget=ManagementPlanField._properties['widget'](
            label='Management_plan',
            label_msgid='indicators_label_management_plan',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
            label='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        required=False,
        accessor="Title",
        searchable=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Assessment_schema = ATFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Assessment_schema['management_plan'] = ManagementPlanField(
        name='management_plan',
        languageIndependent=True,
        required=False,
        default=(datetime.now().year, ''),
        #validators = ('management_plan_code_validator',),
        vocabulary=DatasetYears(),
        widget = ManagementPlanWidget(
            format="select",
            label="EEA Management Plan",
            description = ("EEA Management plan code."),
            label_msgid='dataservice_label_eea_mp',
            description_msgid='dataservice_help_eea_mp',
            i18n_domain='eea.dataservice',
        )
    )

Assessment_schema['relatedItems'] = EEAReferenceField('relatedItems',
        relationship='relatesTo',
        multivalued=True,
        isMetadata=False,
        widget=EEAReferenceBrowserWidget(
            visible={'view':'invisible', 'edit':'invisible'},
            label='Related Item(s)',
            description='Specify related item(s).',
            ))
finalizeATCTSchema(Assessment_schema)
##/code-section after-schema

class Assessment(ATFolder, ModalFieldEditableAware,  CustomizedObjectFactory, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAssessment)

    meta_type = 'Assessment'
    _at_rename_after_creation = True

    schema = Assessment_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('get_assessments')
    def get_assessments(self):
        parts = self.objectValues('AssessmentPart')
        key = None
        secondary = []
        for part in parts:
            if part.is_key_message():
                key = part
            else:
                secondary.append(part)

        return {
                'key':key,
                'secondary':secondary
                }
    security.declarePublic("Title")
    def Title(self):
        try:
            wftool = getToolByName(self, 'portal_workflow')
        except AttributeError:
            return u"Untitled"  #the object has not finished its creation process
        info = wftool.getStatusOf('indicators_workflow', self)
        if not info:
            return u"Untitled"  #the object has not finished its creation process

        if info['review_state'] == "published":
            time = info['time']
            msg = _("assessment-title-published",
                    default=u"Assessment published ${date}",
                    mapping={'date':u"%s %s" %
                        (time.Mon(), time.year())
                        }
                    )
            return self.translate(msg)
        else:
            time = info['time']
            msg = _("assessment-title-draft",
                    default=u"Assessment DRAFT created ${date}",
                    mapping={'date':u"%s %s" %
                        (time.Mon(), time.year())
                        }
                    )
            return self.translate(msg)

    security.declarePublic('getThemes')
    def getThemes(self):
        return self.aq_parent.getThemes()



registerType(Assessment, PROJECTNAME)
# end of class Assessment

##code-section module-footer #fill in your manual code here
##/code-section module-footer



