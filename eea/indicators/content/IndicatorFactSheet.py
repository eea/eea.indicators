__author__ = """Tiberiu Ichim <unknown>"""
__docformat__ = 'plaintext'

import interfaces
from zope.interface import implements
from Products.Archetypes.atapi import *
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from eea.indicators.config import *
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Title",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
        ),
        schemata="default",
        searchable=True,
        required=True,
        accessor="Title",
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            label="Description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='assessment',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="More updates on",
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        searchable=True,
    ),
    DateTimeField(
        name='assessment_date',
        widget=DateTimeField._properties['widget'](
            label="Assessment Date",
            label_msgid='indicators_label_assessment_date',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='source_code',
        widget=StringField._properties['widget'](
            label="Source code",
            label_msgid='indicators_label_source_code',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='data_source_providers',
        widget=StringField._properties['widget'](
            label="Data Source Providers",
            label_msgid='indicators_label_data_source_providers',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='EEA_responsible',
        widget=StringField._properties['widget'](
            label="Owner",
            label_msgid='indicators_label_EEA_responsible',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='DEV_responsible',
        widget=StringField._properties['widget'](
            label="ID of manager user",
            label_msgid='indicators_label_DEV_responsible',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='data_source_info',
        widget=TextAreaWidget(
            label="Data source info",
            label_msgid='indicators_label_data_source_info',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='priority_data_flows',
        widget=TextAreaWidget(
            label="Priority data flows",
            label_msgid='indicators_label_priority_data_flows',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='policy_question',
        widget=StringField._properties['widget'](
            label="Policy Question",
            label_msgid='indicators_label_policy_question',
            i18n_domain='indicators',
        ),
        searchable=True,
    ),
    StringField(
        name='dpsir',
        widget=SelectionWidget(
            label="DPSIR",
            label_msgid='indicators_label_dpsir',
            i18n_domain='indicators',
        ),
        vocabulary=NamedVocabulary("indicator_dpsir"),
    ),
    EEAReferenceField('relatedItems',
            relationship='relatesTo',
            multivalued=True,
            isMetadata=False,
            widget=EEAReferenceBrowserWidget(
                label='Related Item(s)',
                description='Specify related item(s).',
                ))
),
)

IndicatorFactSheet_schema = ATFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()
IndicatorFactSheet_schema.moveField('relatedItems', after='dpsir')


class IndicatorFactSheet(ATFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IIndicatorFactSheet,
               interfaces.IIndicatorAssessment)

    meta_type = 'IndicatorFactSheet'
    _at_rename_after_creation = True

    schema = IndicatorFactSheet_schema

    security.declarePublic("getGeographicCoverage")
    def getGeographicCoverage(self):
        """ """
        result = {}
        wftool = getToolByName(self, 'portal_workflow')

        for ob in self.getRelatedItems():
            if ob.portal_type == 'EEAFigure':
                state = wftool.getInfoFor(ob, 'review_state', '(Unknown)')
                if state in ['published', 'visible']:
                    for val in ob.getGeographicCoverage():
                        result[val] = val
        return list(result.keys())

    security.declarePublic("getTemporalCoverage")
    def getTemporalCoverage(self):
        """ """
        result = {}
        wftool = getToolByName(self, 'portal_workflow')

        for ob in self.getRelatedItems():
            if ob.portal_type == 'EEAFigure':
                state = wftool.getInfoFor(ob, 'review_state', '(Unknown)')
                if state in ['published', 'visible']:
                    for val in ob.getTemporalCoverage():
                        result[val] = val
        return list(result.keys())

registerType(IndicatorFactSheet, PROJECTNAME)
