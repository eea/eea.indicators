from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.versions.versions import CreateVersion as BaseCreateVersion, create_version as base_create_version
from eea.versions.versions import get_versions_api
from eea.workflow.readiness import ObjectReadinessView
from eea.workflow.interfaces import IValueProvider, IObjectReadiness
from zope.component import getMultiAdapter

import logging
logger = logging.getLogger('eea.indicators')


class IndexPage(BrowserView):
    """The Assessment index page"""


class AggregatedEditPage(BrowserView):
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
        return


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
    #IVersionControl(ver).setVersionId(version_id)   #setting the version ID to the assessments group version id
    ver.reindexObject()
    original.reindexObject()    # _reindex(original)  #some indexed values of the context may depend on versions

    return ver


class WorkflowStateReadiness(ObjectReadinessView):
    """ObjectReadiness customizations"""

    #TODO: translate messages
    #TODO: optimize this class, it should at least memoize the results of calling the checks

    checks = (
        (lambda o:filter(lambda p: not getMultiAdapter((p,
                                                      p.schema['assessment']), IValueProvider).has_value(),
                         o.objectValues("AssessmentPart")),
         'You need to fill in the assessments for all the policy questions'),

        (lambda o:filter(lambda p: not IObjectReadiness(p).is_ready_for('published'),
                                    o.objectValues("AssessmentPart")),
         'You need to meet the publishing requirements for all assessment parts'),

        (lambda o: 'published' != getToolByName(o, 'portal_workflow').getInfoFor(aq_parent(aq_inner(o)), 'review_state'),
        "The parent Specification needs to be published"
        ),
    )

    def is_ready_for(self, state_name):
        if state_name == 'published':
            for checker, error in self.checks:
                if checker(self.context):
                    return False
                return True
        else:
            return super(WorkflowStateReadiness, self).is_ready_for(state_name)

    def get_info_for(self, state_name):
        info = ObjectReadinessView.get_info_for(self, state_name)

        #TODO: add the required fields and info from the assessment parts

        extras = []

        for checker, error in self.checks:
            if checker(self.context):
                extras.append(('error', error))

        info['extra'] = extras
        return info

