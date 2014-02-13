""" Assessment content class and utilities
"""

__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import RichWidget, ComputedField
from Products.Archetypes.atapi import Schema, StringField, TextField
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.EEAContentTypes.content.validators import (
    ManagementPlanCodeValidator,
)
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import datetime
from eea.forms.fields.ManagementPlanField import ManagementPlanField
from eea.forms.widgets.ManagementPlanWidget import ManagementPlanWidget
from eea.indicators import msg_factory as _
from eea.indicators.content.base import CustomizedObjectFactory
from eea.indicators.content.base import ModalFieldEditableAware
from eea.indicators.content.interfaces import IAssessment, IIndicatorAssessment
from eea.relations.field import EEAReferenceField
from eea.relations.widget import EEAReferenceBrowserWidget
from eea.versions.interfaces import IGetVersions
from eea.workflow.interfaces import IHasMandatoryWorkflowFields
from eea.workflow.interfaces import IObjectReadiness
from eea.workflow.utils import ATFieldValueProvider

from Products.EEAContentTypes.interfaces import ITemporalCoverageAdapter

from zope.component import adapts
from zope.interface import implements
import logging
#from eea.versions.versions import get_version_id    #get_versions_api,

logger = logging.getLogger('eea.indicators.content.Assessment')


schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible={'view':'invisible', 'edit':'invisible'},
            label='Title',
            description='Title',
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
            ),
        required=False,
        accessor="Title",
        searchable=True,
        default=u'Assessment',
        ),
    TextField(
        name='key_message',
        allowable_content_types=('text/plain', 'text/structured',
                                 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Key message",
            description=("A short message listing the assessment's key "
                         "findings. It works as a summary/abstract for the "
                         "entire indicator assessment."),
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
        languageIndependent=True,
        required_for_published=True,
        required=False,
        default=(datetime.now().year, ''),
        validators = ('management_plan_code_validator',),
        vocabulary_factory="Temporal coverage",
        widget = ManagementPlanWidget(
            format="select",
            label="EEA Management Plan",
            description=("EEA Management plan code. Internal EEA project "
                         "line code, used to assign an EEA product output to "
                         "a specific EEA project number in the "
                         "management plan."),
            label_msgid='dataservice_label_eea_mp',
            description_msgid='dataservice_help_eea_mp',
            i18n_domain='eea.dataservice',
        )
        ),
    EEAReferenceField(
        name='relatedItems',
        isMetadata=False,
        keepReferencesOnCopy=True,
        multiValued=True,
        relationship='relatesTo',
        #referencesSortable=True,
        widget=EEAReferenceBrowserWidget(
            visible={'view':'invisible', 'edit':'invisible'},
            label='Related Item(s)',
            description='Specify related item(s).',
        )
        ),
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

Assessment_schema = ATFolderSchema.copy() + \
                  getattr(ATFolder, 'schema', Schema(())).copy() + \
                  schema.copy()

finalizeATCTSchema(Assessment_schema)


class Assessment(ATFolder, ModalFieldEditableAware,
                 CustomizedObjectFactory, BrowserDefaultMixin):
    """ Assessment content type
    """
    security = ClassSecurityInfo()

    implements(IAssessment, IIndicatorAssessment, IHasMandatoryWorkflowFields)

    meta_type = 'Assessment'
    _at_rename_after_creation = False

    schema = Assessment_schema

    portlet_readiness = \
          ViewPageTemplateFile('../browser/templates/portlet_readiness.pt')

    security.declarePublic('get_assessments')
    def get_assessments(self):
        """ Returns assessment parts
        """
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
        """ return title based on parent specification title
        """
        parent = aq_parent(aq_inner(self))
        if parent:  # the parent seems to be missing in tests
            spec_title = parent.getTitle()
        else:
            spec_title = "Missing parent"

        title = spec_title
        if isinstance(title, unicode):
            title = title.encode('utf-8')

        try:
            wftool = getToolByName(self, 'portal_workflow')
        except AttributeError:
            # the object has not finished its creation process
            title += ' - newly created assessment'
            return title

        time = self.getEffectiveDate()
        info = wftool.getStatusOf('indicators_workflow', self)

        if not info:
            # the object has not finished its creation process
            title += ' - newly created assessment'
        elif info['review_state'] == "published":
            if time is None:
                time = self.creation_date
                msg = _(u"Assessment published with invalid published date")
                return (title + ' - ' +
                        self.translate(msg).encode('utf-8'))

            msg = _(u"Assessment published ${date}",
                    mapping={'date': u"%s %s" %
                             (time.Mon(), time.year())
                             }
                    )
            title += ' - ' + self.translate(msg).encode('utf-8')
        else:
            if time is None:
                time = self.creation_date
            msg = _(u"Assessment DRAFT created ${date}",
                    mapping={'date': u"%s %s" %
                             (time.Mon(), time.year())
                             }
                    )
            title += ' - ' + self.translate(msg).encode('utf-8')

        return title

    security.declarePublic('Subject')
    def Subject(self):
        """ Overwrite standard Subject method to dynamically get all
            keywords from other objects used in this assessment.
        """
        result = []

        # append assessment's own subjects
        result.extend(self.schema['subject'].getRaw(self))

        for assessment_part in self.objectValues('AssessmentPart'):
            for ob in assessment_part.getRelatedItems():
                if ob.portal_type in ['EEAFigure', 'DavizVisualization']:
                    result.extend(ob.Subject())

        #ZZZ: keywords from datasets, work but needs to be double checked
        #      with content experts
        #spec = aq_parent(aq_inner(self))
        #for ob in spec.getRelatedItems():
        #       if ob.portal_type == 'Data':
        #           result.extend(ob.Subject())

        # return results list without duplicates
        return list(set(result))

    security.declarePublic('getThemes')
    def getThemes(self):
        """ Returns parent themes
        """
        parent = aq_parent(aq_inner(self))
        return parent.getThemes()

    security.declarePublic('SearchableText')
    def SearchableText(self):
        """ Override SearchableText to index codes """
        searchable_text = super(Assessment, self).SearchableText()
        for code in self.get_codes():
            searchable_text += '%s ' % code.encode('utf-8')
        for code in self.getCodes():
            if code:
                searchable_text += '%s ' % code['code'].encode('utf-8')
        return searchable_text

    security.declarePublic("Description")
    def Description(self):
        """ Returns description
        """
        convert = getToolByName(self, 'portal_transforms').convert
        text = convert('html_to_text', self.getKey_message()).getData()
        try:
            text = text.decode('utf-8', 'replace')
        except UnicodeDecodeError, err:
            logger.info(err)
        return text

    security.declarePublic("getGeographicCoverage")
    def getGeographicCoverage(self):
        """ Return geographic coverage

        This is only used in the @@esms.xml view
        """
        result = []
        wftool = getToolByName(self, 'portal_workflow')

        for assessment_part in self.objectValues('AssessmentPart'):
            for ob in assessment_part.getRelatedItems():
                if ob.portal_type in ['EEAFigure', 'DavizVisualization']:
                    state = wftool.getInfoFor(ob, 'review_state', '(Unknown)')
                    if state in ['published', 'visible']:
                        result.extend(ob.getLocation())
        return sorted(set(result))

    security.declarePublic("getTemporalCoverage")
    def getTemporalCoverage(self):
        """ Return temporal coverage
        """
        result = {}
        wftool = getToolByName(self, 'portal_workflow')

        for assessment_part in self.objectValues('AssessmentPart'):
            for ob in assessment_part.getRelatedItems():
                if ob.portal_type in ('EEAFigure', 'DavizVisualization'):
                    state = wftool.getInfoFor(ob, 'review_state', '(Unknown)')
                    if state in ['published', 'visible']:
                        temporal_coverage = ITemporalCoverageAdapter(ob
                                                                    ).value()
                        for val in temporal_coverage:
                            result[val] = val
        return list(result.keys())

    security.declarePublic("published_readiness")
    def published_readiness(self):
        """ Used as index for readiness
        """
        return IObjectReadiness(self).get_info_for('published')['rfs_done']

    security.declarePublic("comments")
    def comments(self):
        """ Return the number of comments
        """

        thread = self.plone_utils.getDiscussionThread(self)
        return len(thread) - 1

def hasWrongVersionId(context):
    """ Determines if the assessment belongs to a wrong version group
    """

    cat = getToolByName(context, 'portal_catalog')

    # parent based checks; this also does codes check because
    # assessments inherit codes from their parent specification
    spec = aq_parent(aq_inner(context))
    spec_versions = IGetVersions(spec).versions()
    if not spec in spec_versions:
        spec_versions.append(spec)

    all_assessments = []
    for spec in spec_versions:
        all_assessments.extend(spec.objectValues("Assessment"))

    # now also checking IndicatorFactSheets, using codes to do matching
    codes = ["%s%s" % (c['set'], c['code']) for c in context.getCodes()]
    factsheets = []

    for code in codes:
        factsheets.extend([
            b.getObject() for b in cat.searchResults(
                get_codes=code, portal_type="IndicatorFactSheet")
        ])

    version_ids = {}
    for a in (all_assessments + factsheets):
        vid = IGetVersions(a).versionId
        version_ids[vid] = version_ids.get(vid, []) + [a]

    if len(version_ids) == 1:
        return False

    return True

    #needs python2.5
    #major = max(version_ids.keys(), key_func=lambda k:len(version_ids[k]))

    #major = None
    #for k in version_ids.keys():
        #if not major:
            #major = k
        #if len(version_ids[k]) > len(version_ids[major]):
            #major = k

    #vid = get_version_id(context)
    #return not major == vid


def getPossibleVersionsId(context):
    """ Returns possible version ids that could be attributed to the context
    """
    cat = getToolByName(context, 'portal_catalog')

    spec = aq_parent(aq_inner(context))
    spec_versions = IGetVersions(spec).versions()
    vid = IGetVersions(context).versionId

    all_assessments = []
    for spec in spec_versions:
        all_assessments.extend(spec.objectValues("Assessment"))

    codes = ["%s%s" % (c['set'], c['code']) for c in context.getCodes()]

    factsheets = []
    for code in codes:
        factsheets.extend([
            b.getObject() for b in cat.searchResults(
                get_codes=code, portal_type="IndicatorFactSheet")
        ])

    version_ids = {}
    for a in all_assessments + factsheets:
        vid = IGetVersions(a).versionId
        _asts = version_ids.get(vid, [])
        version_ids[vid] = _asts + [a]

    if len(version_ids) == 1:
        return []

    r = list(set(version_ids) - set([vid]))
    return r


class ManagementPlanFieldValueProvider(ATFieldValueProvider):
    """ Validator
    """
    adapts(Assessment, ManagementPlanField)

    def has_value(self, **kwargs):
        """ Has value?
        """
        vd = ManagementPlanCodeValidator('management_plan_code_validator')
        if not vd(self.get_value()) == 1:
            return False

        return True
