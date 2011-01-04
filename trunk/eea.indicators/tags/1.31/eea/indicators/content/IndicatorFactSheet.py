"""Indicator fact sheet"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes.atapi import Schema, TextField, TextAreaWidget
from Products.Archetypes.atapi import SelectionWidget, ComputedField
from Products.Archetypes.atapi import StringField, RichWidget, DateTimeField
from Products.Archetypes.atapi import registerType
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from eea.indicators.content.IndicatorMixin import IndicatorMixin
from eea.indicators.content.utils import get_dgf_value
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
from zope.interface import implements


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
        allowable_content_types=('text/plain', 'text/structured', 
            'text/html', 'application/msword',),
        widget=RichWidget(
            label="Assessment",
            label_msgid='indicators_label_assessment',
            i18n_domain='indicators',
        ),
        default_output_type='text/html',
        searchable=True,
    ),
    DateTimeField(
        name='assessment_date',
        widget=DateTimeField._properties['widget'](
            label="Assessment date",
            description="Date when the assessment analysis was made. "
                        "This does not necesserly coincide with the "
                        "underline data time coverage which can be older.",
            label_msgid='indicators_label_assessment_date',
            i18n_domain='indicators',
        ),
    ),
    DataGridField(
        name='codes',
        widget=DataGridWidget(
            label="Identification codes",
            description="Codes are short names used to identify the indicator"
                        " in question. Code is made up of a SET-ID and an "
                        "CODE-NR, e.g. TERM 002. Multiple codes are allowed, "
                        "since same indicator can be re-used in other "
                        "indicators' sets.",
            columns={'set':SelectColumn("Set ID", 
                vocabulary="get_indicator_codes"), 
                "code":Column("Code number")},
            auto_insert=True,
            label_msgid='indicatorsfactsheet_label_codes',
            i18n_domain='indicators',
            ),
        columns=("set", "code"),
        required_for_published=True,
        searchable = True,
        validators=('unique_specification_code',),
        ),
    StringField(
        name='source_code',
        searchable = True,
        widget=StringField._properties['widget'](
            label="Source code",
            description="another code who may indentify this indicator "
            "in other source databases.",
            label_msgid='indicators_label_source_code',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='data_source_providers',
        searchable = True,
        widget=StringField._properties['widget'](
            label="Data source providers",
            label_msgid='indicators_label_data_source_providers',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='EEA_responsible',
        widget=StringField._properties['widget'](
            label="EEA main responsible person",
            label_msgid='indicators_label_EEA_responsible',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='DEV_responsible',
        widget=StringField._properties['widget'](
            label="Indicator development responsible",
            label_msgid='indicators_label_DEV_responsible',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='data_source_info',
        searchable = True,
        widget=TextAreaWidget(
            label="Data source info",
            label_msgid='indicators_label_data_source_info',
            i18n_domain='indicators',
        ),
    ),
    TextField(
        name='priority_data_flows',
        searchable = True,
        widget=TextAreaWidget(
            label="Priority data flows",
            label_msgid='indicators_label_priority_data_flows',
            i18n_domain='indicators',
        ),
    ),
    StringField(
        name='policy_question',
        searchable = True,
        widget=StringField._properties['widget'](
            label="Policy Question",
            label_msgid='indicators_label_policy_question',
            i18n_domain='indicators',
        ),
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
                )),
    ComputedField(
        name='temporalCoverage',
        expression="context.getTemporalCoverage()",
        widget=ComputedField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
        ),
    ),
    ComputedField(
        name='geographicCoverage',
        expression="context.getGeographicCoverage()",
        widget=ComputedField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
        ),
    ),
),
)

IndicatorFactSheet_schema = ATFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()
IndicatorFactSheet_schema.moveField('relatedItems', after='dpsir')


class IndicatorFactSheet(ATFolder, BrowserDefaultMixin, IndicatorMixin):
    """IndicatorFactSheet content class
    """
    security = ClassSecurityInfo()

    implements(interfaces.IIndicatorFactSheet,
               interfaces.IIndicatorAssessment)

    meta_type = 'IndicatorFactSheet'
    _at_rename_after_creation = True

    schema = IndicatorFactSheet_schema

    security.declarePublic("getGeographicCoverage")
    def getGeographicCoverage(self):
        """ Geographic coverage """
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
        """ temporal coverage"""
        result = {}
        wftool = getToolByName(self, 'portal_workflow')

        for ob in self.getRelatedItems():
            if ob.portal_type == 'EEAFigure':
                state = wftool.getInfoFor(ob, 'review_state', '(Unknown)')
                if state in ['published', 'visible']:
                    for val in ob.getTemporalCoverage():
                        result[val] = val
        return list(result.keys())

    def get_indicator_codes(self):
        "indicator codes"
        atvm = getToolByName(self, ATVOCABULARYTOOL)
        vocab = getattr(atvm, 'indicator_codes')
        return vocab.getDisplayList(self)

    security.declarePublic('Subject')
    def Subject(self):
        """Overwrite standard Subject method to dynamically get all
           keywords from other objects used in this assessment. """
        result = []

        #append assessment own subjects
        result.extend(self.schema['subject'].getRaw(self))

        #append indicator codes
        result.extend(self.get_codes())

        #TODO: append themes, they are tags as well
        #result.extend(self.getThemes())

        for ob in self.getRelatedItems():
            if ob.portal_type == 'EEAFigure':
                result.extend(ob.Subject())

        #return results list without duplicates
        return list(set(result))

    security.declarePublic("getTitle")
    def getTitle(self):
        """ Return title with codes.  """
        codes = self.getCodes()

        res = ''
        for code in codes:
            if code:
                res = res + "%s %s/" % (code['set'], code['code'])
        if res:
            res = self.title + ' (' + res[:-1] + ')'
        else:
            res = self.title
        return res

    security.declarePublic('get_codes')
    def get_codes(self):
        """Returns a list of indicator codes, for indexing.

        Indexes the codes of this specification in the form of
        a KeywordIndex with ['SETA', "SETA001", "SETB", "SETB009"]
        the idea is to be able to search for set code (ex: SETB)
        but also for the full code (ex:SETB009)
        """
        codes = self.getCodes()

        res = []
        for code in codes:
            if code:
                res.extend(
                        [code['set'],
                            "%s%s" % (code['set'], code['code'])]
                        )
        return res

    security.declareProtected("Modify portal content", 'setCodes')
    def setCodes(self, value):
        """Set the codes"""
        #we want to filter rows that don't have a number filled in
        field = self.schema['codes']
        instance = self
        value = get_dgf_value(field, value)
        for row in value:
            try:
                row['code'] = "%03d" % int(row['code'])
            except ValueError:
                continue
        field.getStorage(instance).set(field.getName(), instance, value)

    security.declarePublic('SearchableText')
    def SearchableText(self):
        """Searchable text """
        searchable_text = super(IndicatorFactSheet, self).SearchableText()
        for code in self.get_codes():
            searchable_text += '%s ' % code.encode('utf-8')
        return searchable_text

    security.declarePublic("comments")
    def comments(self):
        """Return the number of comments"""

        try:
            return len(self.getReplyReplies(self))
        except AttributeError:
            return 0    #this happens in tests


registerType(IndicatorFactSheet, PROJECTNAME)
