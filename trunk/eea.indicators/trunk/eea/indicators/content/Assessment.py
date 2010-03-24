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
from datetime import datetime
from eea.dataservice.vocabulary import DatasetYears
from eea.dataservice.widgets.ManagementPlanWidget import ManagementPlanWidget
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
        default_output_type='text/html',
        searchable=True,
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

finalizeATCTSchema(Assessment_schema)
##/code-section after-schema

class Assessment(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAssessment)

    meta_type = 'Assessment'
    _at_rename_after_creation = False

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
        has_versions = self.unrestrictedTraverse('@@hasVersions')()

        if not has_versions:
            msg = _(u"assessment_title_no_versions_msg",
                default=u"Assessment for ${title}",
                mapping={'title':self.aq_parent.getTitle()})
            return self.translate(msg)

        version = 0 #avoids problem in create new version
        versions = self.unrestrictedTraverse('@@getVersions')()

        for k,v in versions.items():    #this is a dict {1:<Spec>, 2:<Spec>}
            if v.getPhysicalPath() == self.getPhysicalPath():
                version = k
                break

        msg = _(u"specification_title_msg",
                default=u"Assessment for ${title} (version ${version})",
                mapping={'title':self.aq_parent.getTitle(), 'version':version})

        return self.translate(msg)

    security.declarePublic('getThemes')
    def getThemes(self):
        return self.aq_parent.getThemes()



registerType(Assessment, PROJECTNAME)
# end of class Assessment

##code-section module-footer #fill in your manual code here
##/code-section module-footer



