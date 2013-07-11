""" Assessment controllers
"""

from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZPublisher.Client import querify
from eea.indicators.browser.utils import has_one_of
from eea.indicators.content.Assessment import getPossibleVersionsId
from eea.indicators.content.Assessment import hasWrongVersionId
from eea.versions.interfaces import IGetVersions
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import create_version as base_create_version
from eea.workflow.interfaces import IObjectReadiness
from eea.workflow.readiness import ObjectReadiness
from lxml.builder import ElementMaker
from plone.app.layout.globals.interfaces import IViewView
from zope.event import notify
from zope.interface import implements
import datetime
import lxml

#from eea.versions.versions import get_version_id
#from eea.versions.versions import get_versions_api

class IndexPage(BrowserView):
    """The Assessment index page"""


class AggregatedEditPage(BrowserView):
    """Aggregated edit"""
    implements(IViewView)
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


class AssessmentAsXML(BrowserView):
    """The @@xml view according to ESTAT specification
    """

    def __call__(self):
        self.request.response.setHeader('Content-Type','text/xml')

        now = datetime.datetime.now()
        year_start = datetime.datetime(year=now.year, month=1, day=1)
        year_end = datetime.datetime(year=now.year, month=12, day=31)
        #maybe it should be done as timedelta of 1sec from previous year

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
                    M.ComponentValue("2013-A0", component="TIME_PERIOD", object="TimeDimension"),   #TODO: Check here
                    M.ComponentValue("4D0", component="DATA_PROVIDER", object="DataProvider"),
                    M.ComponentValue("B5_ESMSIPEEA_A", component="DATAFLOW", object="DataFlow"),
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
                        M.Value('Martin Adam'), #TODO: FIXME
                        conceptID="CONTACT_NAME", 
                    ),
                    M.ReportedAttribute(
                        M.Value('Not available'),
                        conceptID="CONTACT_FUNC", 
                    ),
                    M.ReportedAttribute(
                        M.Value('Kongens Nytorv 6, 1050, Copenhagen K, Denmark'),
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
                        M.Value('Not available'),
                        conceptID="CONTACT_FAX", 
                    ),
                    conceptID="CONTACT",
                ),
                M.ReportedAttribute(    #META_UPDATE
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value('2012-12-21'),
                        conceptID="META_CERTIFIED", 
                    ),
                    M.ReportedAttribute(
                        M.Value('2012-12-21'),
                        conceptID="META_POSTED", 
                    ),
                    M.ReportedAttribute(
                        M.Value('2012-12-21'),
                        conceptID="META_LAST_UPDATE", 
                    ),
                    conceptID="META_UPDATE",
                ),
                M.ReportedAttribute(    #STAT_PRES
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(self.context.Description()),
                        conceptID="DATA_DESCR", 
                    ),
                    M.ReportedAttribute(
                        M.Value(),  #TODO
                        conceptID="CLASS_SYSTEM", 
                    ),
                    M.ReportedAttribute(
                        M.Value(),  #TODO
                        conceptID="COVERAGE_SECTOR", 
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="STAT_CONC_DEF", 
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="STAT_UNIT", 
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="STAT_POP", 
                    ),
                    M.ReportedAttribute(
                        M.Value(),  #TODO
                        conceptID="COVERAGE_TIME", 
                    ),
                    M.ReportedAttribute(
                        M.Value("Not available"),
                        conceptID="BASE_PER", 
                    ),
                    conceptID="STAT_PRES"
                ),
                M.ReportedAttribute(
                    M.Value(),  #TODO
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
"http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32009R0401:EN:NOT)"),
                        conceptID="INST_MAN_LA_OA", 
                    ),
                    M.ReportedAttribute(
                        M.Value("Regulation (EC) No 401/2009 of the European "
"Parliament and of the Council of 23 April 2009 (available at "
"http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32009R0401:EN:NOT)"),
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
                    conceptID="DISS_FORMAT", 
                ),
                M.ReportedAttribute(    #ACCESS_DOC
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(),      #TODO
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
                        M.Value(),  #TODO
                        conceptID="QUALITY_ASSMNT", 
                    ),
                    conceptID="QUALITY_MGMNT", 
                ),
                M.ReportedAttribute(    #RELEVANCE
                    M.Value(),
                    M.ReportedAttribute(
                        M.Value(),  #TODO
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
                    conceptID="QUALITY_MGMNT", 
                ),
            ),
        )

        root = lxml.etree.Element(nsel("GenericMetadata"), nsmap=NAMESPACES)
        root.append(header)
        root.append(metadata)

        return lxml.etree.tostring(root)

