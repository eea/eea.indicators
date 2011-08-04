from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.browser.utils import has_one_of
from eea.indicators.content.Assessment import getPossibleVersionsId
from eea.indicators.content.Assessment import hasWrongVersionId
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import create_version as base_create_version
from eea.versions.versions import get_version_id
from eea.versions.versions import get_versions_api
from eea.workflow.interfaces import IObjectReadiness
from eea.workflow.readiness import ObjectReadiness
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implements


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
        latest = get_versions_api(spec).latest_version()

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
            return self.request.RESPONSE.redirect(version.absolute_url())

        if choice == "newest":
            version = latest.factory_Assessment()['obj']
            return self.request.RESPONSE.redirect(version.absolute_url())

        raise ValueError("Unknown option for field choice")


def create_version(original, request=None):
    """Creates a new version of an Assessment. Returns the new version object
    """
    #TODO: check if the following is still applied. It is true in any case
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

    #TODO: should we reindex the objects here?
    for obj in ver.objectValues():
        obj.setEffectiveDate(None)
        obj.setCreationDate(DateTime())

    #The links to EEAFigures are updated to point to their latest version

    assessment = ver

    for ap in assessment.objectValues("AssessmentPart"):
        rels = []
        for o in ap.getRelatedItems():
            if o.meta_type == "EEAFigure":
                api = get_versions_api(o)
                new = api.latest_version()
                if new:
                    rels.append(new)
                else:
                    rels.append(o)
            else:
                rels.append(o)

        ap.setRelatedItems(rels)
        ap.reindexObject()

    # Set new state
    #IVersionControl(ver).setVersionId(version_id)   
    #setting the version ID to the assessments group version id
    ver.reindexObject()
    original.reindexObject()    # _reindex(original)  
    #some indexed values of the context may depend on versions

    return ver


class WorkflowStateReadiness(ObjectReadiness):
    """ObjectReadiness customizations"""

    #TODO: translate messages

    checks = {'published':(
        (lambda o:hasWrongVersionId(o),
        'This Assessment belongs to the wrong version group. To fix this '
        'please visit the Indicator Specification edit page.'),

        (lambda o:filter(
            lambda p: not IObjectReadiness(p).is_ready_for('published'),
                                    o.objectValues("AssessmentPart")),
        'You need to fill in the assessments for all the policy questions'),

        (lambda o:not IObjectReadiness(
                           aq_parent(aq_inner(o))).is_ready_for('published'),
         "You need to finish the <a href='../'>"
         "Indicator Specification</a> first!"),

        (lambda o: 'published' != getToolByName(o, 'portal_workflow').
                            getInfoFor(aq_parent(aq_inner(o)), 'review_state'),
        "The Indicator Specification needs to be published"
        ),
        (lambda o:not filter(lambda part: has_one_of(["EEAFigure"], 
                    part.getRelatedItems()), o.objectValues("AssessmentPart")),
        "The answered policy questions need to point to at least one Figure"),
    )}

    @property
    def depends_on(self):
        """see interface"""
        return self.context.objectValues("AssessmentPart")


class WrongVersionReport(BrowserView):
    """Reports what's wrong with the current version id of an assessment"""

    def current_version(self):
        """current version"""
        return get_version_id(self.context)

    def possible_versions(self):
        """possible versions"""
        versions = getPossibleVersionsId(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')

        res = {}
        for v in versions:
            res[v] = map(
                    lambda b:b.getObject(),
                    catalog.searchResults(getVersionId=v))

        return res

    def get_version_for(self, obj):
        """get version for"""
        return get_version_id(obj)
