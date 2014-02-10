# -*- coding: utf-8 -*-
""" Assessment controllers
"""

from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZPublisher.Client import querify
from bs4 import UnicodeDammit, BeautifulSoup
from eea.indicators.browser.utils import has_one_of
from eea.indicators.browser.interfaces import IIMSBaseView
from eea.indicators.content.Assessment import getPossibleVersionsId
from eea.indicators.content.Assessment import hasWrongVersionId
from eea.versions.interfaces import IGetVersions
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import create_version as base_create_version
from eea.workflow.interfaces import IObjectReadiness
from eea.workflow.readiness import ObjectReadiness
from lxml.builder import ElementMaker
from plone.app.layout.globals.interfaces import IViewView
from zope.component import getMultiAdapter
from zope.event import notify
from zope.interface import implements
import datetime
import logging
import lxml

logger = logging.getLogger("eea.indicators.browser.assessment")


class IndexPage(BrowserView):
    """The Assessment index page"""
    implements(IIMSBaseView)

    def getId(self):
        return "view"


class AggregatedEditPage(BrowserView):
    """Aggregated edit"""
    implements(IViewView, IIMSBaseView)
    template = ViewPageTemplateFile('templates/assessment/aggregated_edit.pt')

    __call__ = template


class CreateVersion(BaseCreateVersion):
    """Create new version customizations for eea.versions """

    template = ViewPageTemplateFile('templates/assessment/create_version.pt')
    newer_spec = None

    def __call__(self):
        spec = aq_parent(aq_inner(self.context))
        latest = IGetVersions(spec).latest_version()

        if spec.UID() == latest.UID():
            version = create_version(self.context)
            return self.request.RESPONSE.redirect(version.absolute_url())

        self.spec_title = latest.Title()
        self.spec_url = latest.absolute_url()
        self.date = latest.effective_date or latest.creation_date
        if "submit" not in self.request.form:
            return self.template()

        choice = self.request.form.get("choice")

        if choice == "here":
            version = create_version(self.context)
            #return self.request.RESPONSE.redirect(version.absolute_url())
            return "OK"

        if choice == "newest":
            version = latest.factory_Assessment()['obj']
            #return self.request.RESPONSE.redirect(version.absolute_url())
            return "OK"

        raise ValueError("Unknown option for field choice")

    def create(self):
        """ Because this view is more complex, we do the actual version creation
        in the __call__
        """
        raise NotImplementedError


class CreateVersionAjax(BaseCreateVersion):
    """ The @@createVersionAjax override view for Assessments

    Due to the use of the background creation of versions, we need to
    tell eea.versions that, in some cases, we have a separate page
    where we ask the user to make a choice.
    """

    def __call__(self):
        spec = aq_parent(aq_inner(self.context))
        latest = IGetVersions(spec).latest_version()

        if spec.UID() == latest.UID():
            create_version(self.context)
            return "OK"

        return "SEEURL: %s/@@createVersion" % self.context.absolute_url()


def create_version(original, request=None):
    """Creates a new version of an Assessment. Returns the new version object
    """
    #ZZZ: check if the following is still applied. It is true in any case
    #we want all Assessments for all spec versions to have the
    #same version id.
    #>>>if the parent Specification has versions, then the Assessment
    #needs to be a version of those assessments
    ver = base_create_version(original, reindex=False)

    # The assessment is no longer effective
    ver.setEffectiveDate(None)
    ver.setCreationDate(DateTime())

    # Delete comment files
    file_ids = []
    for file_ob in ver.getFolderContents(contentFilter={'portal_type':'File'},
            full_objects=True):
        file_ids.append(file_ob.getId())
    ver.manage_delObjects(ids=file_ids)

    #ZZZ: should we reindex the objects here?
    for obj in ver.objectValues():
        obj.setEffectiveDate(None)
        obj.setCreationDate(DateTime())

    # The links to EEAFigures are updated to point to their latest version
    # Also, we need to add whatever new PolicyQuestions were added in
    # the Specification

    assessment = ver

    spec = assessment.aq_parent
    pqs = set(spec.objectIds("PolicyQuestion"))
    assigned_pqs = set()

    for ap in assessment.objectValues("AssessmentPart"):
        rels = []
        for o in ap.getRelatedItems():
            if o.meta_type == "EEAFigure":
                rels.append(IGetVersions(o).latest_version())
            elif o.meta_type == "PolicyQuestion":
                rels.append(o)
                assigned_pqs.add(o.getId())
            else:
                rels.append(o)

        ap.set_related_items(rels)
        ap.reindexObject()

    #creating missing policy questions
    new_pqs = pqs - assigned_pqs
    for oid in new_pqs:
        aid = assessment.invokeFactory(type_name="AssessmentPart",
                id=assessment.generateUniqueId("AssessmentPart"),)
        ap = assessment[aid]
        ap.set_related_items(spec[oid])
        try:
            ap.reindexObject()
        except AttributeError:
            continue

    # Set new state
    #IVersionControl(ver).setVersionId(version_id)
    #setting the version ID to the assessments group version id
    ver.reindexObject()
    notify(ObjectInitializedEvent(ver))
    original.reindexObject()    # _reindex(original)
    #some indexed values of the context may depend on versions

    return ver


def hasUnpublishableFigure(ast):
    """ Assessment has a relation to a figure that's not publishable?

    Also check that the figure is actually publishable
    """

    wftool = getToolByName(ast, 'portal_workflow')

    for part in ast.objectValues("AssessmentPart"):
        figures = [f for f in part.getRelatedItems()
                        if f.portal_type in ('EEAFigure',
                                             'DavizVisualization')]
        for fig in figures:
            #skip published figures
            if wftool.getInfoFor(fig, 'review_state') == 'published':
                continue
            #fail on not finished figures
            if not IObjectReadiness(fig).is_ready_for('published'):
                return True
            #check that the figures are actually publishable
            if not [t for t in wftool.getTransitionsFor(fig) if
                    t['id'] in ('publish', 'quickPublish')]:
                return True

    return False


class WorkflowStateReadiness(ObjectReadiness):
    """ObjectReadiness customizations"""

    #ZZZ: translate messages

    checks = {'published':(

        (lambda o:hasWrongVersionId(o),
        'This Assessment belongs to the wrong version group. To fix this '
        'please visit the Indicator Specification edit page.'),

        (lambda o: bool([p for p in o.objectValues("AssessmentPart")
                        if not IObjectReadiness(p).is_ready_for('published')]),
        'You need to fill in the assessments for all the policy questions.'),

        (lambda o:not IObjectReadiness(
                           aq_parent(aq_inner(o))).is_ready_for('published'),
     "You need to finish the <a href='../'>Indicator Specification</a> first!"),

        (lambda o: 'published' != getToolByName(o, 'portal_workflow').
                            getInfoFor(aq_parent(aq_inner(o)), 'review_state'),
        "The Indicator Specification needs to be published."
        ),

        (lambda o: not [part for part in o.objectValues("AssessmentPart")
                        if has_one_of(["EEAFigure", "DavizVisualization"],
                                      part.getRelatedItems())],
        "The answered policy questions need to point to at least one "
        "Figure or Daviz Visualization."),

        (lambda o:hasUnpublishableFigure(o),
        'Some of the figures in this indicator are not completed, please check'
        ' each of the figures to see what required information is missing.'),

    )}

    @property
    def depends_on(self):
        """see interface"""
        return self.context.objectValues("AssessmentPart")


class WrongVersionReport(BrowserView):
    """Reports what's wrong with the current version id of an assessment"""

    def current_version(self):
        """current version"""
        return IGetVersions(self.context).versionId

    def possible_versions(self):
        """possible versions"""
        versions = getPossibleVersionsId(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')

        res = {}
        for v in versions:
            res[v] = [b.getObject()
                      for b in catalog.searchResults(getVersionId=v)]
        return res

    def get_version_for(self, obj):
        """get version for"""
        return IGetVersions(obj).versionId


class FragmentMetadataView(BrowserView):
    """View for fragment_metadata
    """

    schematas = ['categorization', 'dates', 'ownership', 'settings']
    exclude = ['relatedItems', 'subject']   #'location',  'subject'

    def field_names(self):
        """ field names"""
        c = self.context
        fields = c.schema.filterFields(lambda f:f.schemata in self.schematas)
        fields = [f.getName() for f in fields if f.getName() not
                                                        in self.exclude]

        return fields

    def fields(self):
        """returns a query for fields
        """
        return querify([('fields', self.field_names())])


NAMESPACES = {  #shortcut:full ns
    None:"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
    'GenericMetadata':
        "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/genericmetadata",
    'common':"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
    'compact':"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
    'cross':"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross",
    'generic':"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic",
    'structure':"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
    'xsi':"http://www.w3.org/2001/XMLSchema-instance",
}


def nsel(el, ns=None):
    """Returns a proper string for lxml to construct a namespaced element
    """
    return "{%s}%s" % (NAMESPACES[ns], el)


def escapeSpecialChars(value):
    """ Replace special characters.
    """
    return value.replace("–", "-").replace("±", "+/-")\
        .replace("\xe2\x80\x94", "-")


def _toUnicode(value):
    """Convert an unknown string to unicode
    """
    if not isinstance(value, unicode):
        value = UnicodeDammit(value).unicode_markup
    return value



class MetadataAsESMSXML(BrowserView):
    """The XML output according to Euro SDMX metadata structure (ESMS).
    """

    def __call__(self):
        self.request.response.setHeader('Content-Type','text/xml')

        now = datetime.datetime.now()
        year_start = datetime.datetime(year=now.year, month=1, day=1)
        year_end = datetime.datetime(year=now.year, month=12, day=31)
        #maybe it should be done as timedelta of 1sec from previous year

        def getTextKeepHTML(value):
            value = escapeSpecialChars(value)
            return _toUnicode("<![CDATA[{0}]]".format((value)))

        def getTextStripHTML(value):
            value = escapeSpecialChars(value)
            return BeautifulSoup(value).get_text()

        getText = getTextKeepHTML \
            if self.request.get("keepHTML", "false") == "true"\
            else getTextStripHTML


        #we extract some info here to simplify code down below
        spec = self.context.aq_parent

        effective = self.context.getEffectiveDate()
        if effective:
            publish_date = effective.asdatetime().date().isoformat()
        else:
            publish_date = ""

        spec_modified = spec.modified().asdatetime().date().isoformat()
        latest_version = IGetVersions(self.context).latest_version()

        ref_area = u", ".join([c.decode('utf-8') for c in
                              self.context.getGeographicCoverage()])

        manager_id = spec.getManager_user_id()
        mtool = getToolByName(spec, 'portal_membership')
        manager_name = (mtool.getMemberInfo(manager_id)
                        or {}).get('fullname', 'Missing')
        manager_name = manager_name.decode('utf-8')

        dpsir_vocab = NamedVocabulary('indicator_dpsir'
                                        ).getVocabularyDict(spec)
        typology_vocab = NamedVocabulary('indicator_typology'
                                        ).getVocabularyDict(spec)

        dpsir = dpsir_vocab.get(spec.getDpsir())
        typology = typology_vocab.get(spec.getTypology())
        dpsir_typology = "DPSIR: %s - Typology: %s" % (dpsir, _toUnicode(typology))

        themes_vocab = dict(spec._getMergedThemes())
        themes = ", ".join([themes_vocab.get(l) for l in spec.getThemes()])

        #let's use the already well-formatted temporal coverage browser view
        temporal_coverage = getMultiAdapter(
            (self.context, self.request), name=u'formatTempCoverage')()

        units = getText(spec.getUnits()) or u'Not available'

        data_sets = [rel for rel in spec.getRelatedItems()
                        if rel.portal_type == 'Data']
        ext_data_sets = [rel for rel in spec.getRelatedItems()
                        if rel.portal_type == 'ExternalDataSpec']

        out = ""

        for dataowner in data_sets:
            out += u" ".join((_toUnicode(dataowner.Title()),
                                    dataowner.absolute_url()))
            out += u" "
            for provider_url in dataowner.getDataOwner():
                org = spec.getOrganisationName(provider_url)
                if org:
                    out += u" ".join((_toUnicode(org.Title),
                                            provider_url))
                    out += u" "

        for eds in ext_data_sets:
            out += u" ".join((_toUnicode(eds.Title()),
                                    eds.absolute_url()))
            out += u" "
            org = spec.getOrganisationName(eds.getProvider_url())
            if org:
                out += u" ".join((_toUnicode(org.Title),
                                        eds.getProvider_url()))
                out += u" "

        mrefs = [b.getObject() for b in spec.getFolderContents(
                        contentFilter={'portal_type':'MethodologyReference'})]

        methodology_reference = getText(
            "\n".join(
                [(o.Title() + "\n" + o.getDescription()) for o in mrefs]))


        uncertainties = getText('Methodology uncertainty: ' +\
                                spec.getMethodology_uncertainty() +\
                                '\nData uncertainty: ' +\
                                spec.getData_uncertainty() +\
                                '\nRationale uncertainty: ' +\
                                spec.getRationale_uncertainty())

        questions = [b.getObject() for b in spec.getFolderContents(
                        contentFilter={'portal_type':'PolicyQuestion'})]
        qpart = ""
        if questions:
            main_q = None
            for q in questions:
                if q.getIs_key_question():
                    main_q = q
            if main_q is not None:
                qpart += "Key policy question: %s\n" % main_q.Title()

            for q in questions:
                if q == main_q:
                    continue
                qpart += "Specific policy question: %s\n" % q.Title()

        user_needs = getText('Justification for indicator selection: '+\
                             spec.getRationale_justification()+ "\n" + qpart)

        methodology = getText(spec.getMethodology())
        methodology_gapfilling = getText(spec.getMethodology_gapfilling())
        indicator_definition = getText(spec.Title() + ". " + \
                                       spec.getDefinition())
        frequency_of_updates = getText(spec.get_frequency_of_updates())

        #The xml construction
        E = ElementMaker(nsmap=NAMESPACES)

        header = E.Header(
            E.ID("B5_ESMSIPEEA_A"),
            E.Prepared(now.isoformat()),
            E.Sender(id="4D0"),
            E.DataSetID("MDF_B5_ESMSIPEEA_A_1353407791410"),
            E.DataSetAction("Append"),
            E.Extracted(now.isoformat()),
            E.ReportingBegin(year_start.isoformat()),
            E.ReportingEnd(year_end.isoformat()),
        )

        M = ElementMaker(namespace=NAMESPACES['GenericMetadata'],
                         nsmap=NAMESPACES)

        metadata = M.MetadataSet(
            M.MetadataStructureRef('ESMSIPEEA_MSD'),
            M.MetadataStructureAgencyRef("ESTAT"),
            M.ReportRef('ESMS_REPORT_FULL'),
            M.AttributeValueSet(
                M.TargetRef("FULL_ESMS"),
                M.TargetValues(
                    M.ComponentValue("2013-A0", component="TIME_PERIOD",
                                     object="TimeDimension"),
                    M.ComponentValue("4D0", component="DATA_PROVIDER",
                                     object="DataProvider"),
                    M.ComponentValue("B5_ESMSIPEEA_A", component="DATAFLOW",
                                     object="DataFlow"),
                ),
                M.ReportedAttribute(    #CONTACT
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value('European Environment Agency (EEA)'),
                        conceptID="CONTACT_ORGANISATION",
                    ),
                    M.ReportedAttribute(
                        M.Value('Not available'),
                        conceptID="ORGANISATION_UNIT",
                    ),
                    M.ReportedAttribute(
                        M.Value(manager_name),
                        conceptID="CONTACT_NAME",
                    ),
                    M.ReportedAttribute(
                        M.Value('Not available'),
                        conceptID="CONTACT_FUNC",
                    ),
                    M.ReportedAttribute(
                        M.Value('Kongens Nytorv 6, 1050, '
                                'Copenhagen K, Denmark'),
                        conceptID="CONTACT_MAIL",
                    ),
                    M.ReportedAttribute(
                        M.Value('Not available'),
                        conceptID="CONTACT_EMAIL",
                    ),
                    M.ReportedAttribute(
                        M.Value('Not available'),
                        conceptID="CONTACT_PHONE",
                    ),
                    M.ReportedAttribute(
                        M.Value('Not applicable'),
                        conceptID="CONTACT_FAX",
                    ),
                    conceptID="CONTACT",
                ),
                M.ReportedAttribute(    #META_UPDATE
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(publish_date),
                        conceptID="META_CERTIFIED",
                    ),
                    M.ReportedAttribute(
                        M.Value(publish_date),
                        conceptID="META_POSTED",
                    ),
                    M.ReportedAttribute(
                        M.Value(spec_modified),
                        conceptID="META_LAST_UPDATE",
                    ),
                    conceptID="META_UPDATE",
                ),
                M.ReportedAttribute(    #STAT_PRES
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(indicator_definition),
                        conceptID="DATA_DESCR",
                    ),
                    M.ReportedAttribute(
                        M.Value(dpsir_typology),
                        conceptID="CLASS_SYSTEM",
                    ),
                    M.ReportedAttribute(
                        M.Value(themes),
                        conceptID="COVERAGE_SECTOR",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="STAT_CONC_DEF",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="STAT_UNIT",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="STAT_POP",
                    ),
                    M.ReportedAttribute(
                        M.Value(ref_area),
                        conceptID="REF_AREA",
                    ),
                    M.ReportedAttribute(
                        M.Value(temporal_coverage),
                        conceptID="COVERAGE_TIME",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="BASE_PER",
                    ),
                    conceptID="STAT_PRES"
                ),
                M.ReportedAttribute(
                    M.Value(units),
                    conceptID="UNIT_MEASURE",
                ),
                M.ReportedAttribute(
                    M.Value("Not available"),
                    conceptID="REF_PERIOD",
                ),
                M.ReportedAttribute(    #INST_MANDATE
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Regulation (EC) No 401/2009 of the European "
"Parliament and of the Council of 23 April 2009 (available at "
"http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri="
"CELEX:32009R0401:EN:NOT)"),
                        conceptID="INST_MAN_LA_OA",
                    ),
                    M.ReportedAttribute(
                        M.Value("Regulation (EC) No 401/2009 of the European "
"Parliament and of the Council of 23 April 2009 (available at "
"http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri="
"CELEX:32009R0401:EN:NOT)"),
                        conceptID="INST_MAN_SHAR",
                    ),
                    conceptID="INST_MANDATE",
                ),
                M.ReportedAttribute(    #CONF
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="CONF_DATA_TR",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="CONF_POLICY",
                    ),
                    conceptID="CONF",
                ),
                M.ReportedAttribute(    #REL_POLICY
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="REL_CAL_POLICY",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="REL_CAL_ACCESS",
                    ),
                    M.ReportedAttribute(
                        M.Value("All EEA indicators are public"),
                        conceptID="REL_POL_US_AC",
                    ),
                    conceptID="REL_POLICY",
                ),
                M.ReportedAttribute(
                    M.Value("Not available"),
                    conceptID="FREQ_DISS",
                ),
                M.ReportedAttribute(
                    M.Value("Not available"),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="NEWS_REL",
                    ),
                    M.ReportedAttribute(
                        M.Value(latest_version.absolute_url()),
                        conceptID="PUBLICATIONS",
                    ),
                    M.ReportedAttribute(
                        M.Value(
                        "http://www.eea.europa.eu/data-and-maps/indicators"),
                        conceptID="ONLINE_DB",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="MICRO_DAT_ACC",
                    ),
                    M.ReportedAttribute(
                        M.Value("Twitter: Indicators are automatically "
"announced via EEA's Twitter channel (https://twitter.com/euenvironment), "
"which users can follow. RSS feed: Indicators are automatically "
"announced in a dedicated EEA indicators RSS feed "
"(http://www.eea.europa.eu/data-and-maps/indicators/RSS2), which users can "
"subscribe to. A catalogue of all indicators is available "
"(http://www.eea.europa.eu/data-and-maps/indicators)."),
                        conceptID="DISS_OTHER",
                    ),
                    conceptID="DISS_FORMAT",
                ),
                M.ReportedAttribute(    #ACCESS_DOC
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(methodology_reference),
                        conceptID="DOC_METHOD",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="QUALITY_DOC",
                    ),
                    conceptID="ACCESS_DOC",
                ),
                M.ReportedAttribute(    #QUALITY_MGMNT
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="QUALITY_ASSURE",
                    ),
                    M.ReportedAttribute(
                        M.Value(uncertainties),
                        conceptID="QUALITY_ASSMNT",
                    ),
                    conceptID="QUALITY_MGMNT",
                ),
                M.ReportedAttribute(    #RELEVANCE
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(user_needs),
                        conceptID="USER_NEEDS",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="USER_SAT",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="COMPLETENESS",
                    ),
                    conceptID="RELEVANCE",
                ),
                M.ReportedAttribute(    #ACCURACY
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="ACCURACY_OVERALL",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="SAMPLING_ERR",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="NONSAMPLING_ERR",
                    ),
                    conceptID="ACCURACY",
                ),
                M.ReportedAttribute(    #TIMELINESS_PUNCT
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="TIMELINESS",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="PUNCTUALITY",
                    ),
                    conceptID="TIMELINESS_PUNCT",
                ),
                M.ReportedAttribute(    #COMPARABILITY
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        M.ReportedAttribute(
                            M.Value("Not available"),
                            conceptID="COMPAR_GEO_COVER",
                        ),
                        M.ReportedAttribute(
                            M.Value("Not available"),
                            conceptID="COMPAR_GEO_COMMENT",
                        ),
                        conceptID="COMPAR_GEO",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        M.ReportedAttribute(
                            M.Value("Not available"),
                            conceptID="COMPAR_TIME_COVER",
                        ),
                        M.ReportedAttribute(
                            M.Value("Not available"),
                            conceptID="COMPAR_TIME_COMMENT",
                        ),
                        conceptID="COMPAR_TIME",
                    ),
                    conceptID="COMPARABILITY",
                ),
                M.ReportedAttribute(    #COHERENCE
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Not applicable"),
                        conceptID="COHER_X_DOM",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="COHER_INTERNAL",
                    ),
                    conceptID="COHERENCE",
                ),
                M.ReportedAttribute(
                    M.Value("Not applicable"),
                    conceptID="COST_BURDEN",
                ),
                M.ReportedAttribute(    #DATA_REV
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value("Indicator assessments are peer reviewed and "
"CSIs go under extended country review process. Previous versions of "
"indicators are available. Data coming from EEA's data flows have their own "
"QA procedure. The quality of third part data is under responsibily of "
"respective data providers."),
                        conceptID="REV_POLICY",
                    ),
                    M.ReportedAttribute(
                        M.Value("Indicator assessments are peer reviewed and "
"CSIs go under extended country review process. Previous versions of "
"indicators are available. Data coming from EEA's data flows have their own "
"QA procedure. The quality of third part data is under responsibily of "
"respective data providers."),
                        conceptID="REV_PRACTICE",
                    ),
                    conceptID="DATA_REV",
                ),
                M.ReportedAttribute(    #STAT_PROCESS
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(out),
                        conceptID="SOURCE_TYPE",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="FREQ_COLL",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="COLL_METHOD",
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="DATA_VALIDATION",
                    ),
                    M.ReportedAttribute(
                        M.Value(methodology),
                        conceptID="DATA_COMP",
                    ),
                    M.ReportedAttribute(
                        M.Value(methodology_gapfilling),
                        conceptID="ADJUSTMENT",
                    ),
                    M.ReportedAttribute(
                        M.Value(frequency_of_updates),
                        conceptID="FREQ_DISS",
                    ),
                    conceptID="STAT_PROCESS",
                ),
                M.ReportedAttribute(
                    M.Value("Please note that more metadata and additional "
"information about this indicator is available online at %s. For technical "
"issues contact EEA web team at http://www.eea.europa.eu/help/contact-info. "
"Metadata extracted automatically by EEA IMS at %s." %
(self.context.absolute_url(), now.isoformat())),
                    conceptID="COMMENT_DSET",
                ),
            ),
        )

        root = lxml.etree.Element(nsel("GenericMetadata"), nsmap=NAMESPACES)
        root.append(header)
        root.append(metadata)

        return lxml.etree.tostring(root)
