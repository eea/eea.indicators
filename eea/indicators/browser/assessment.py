from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import parent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import CreateVersion as BaseCreateVersion, create_version as base_create_version
from eea.versions.versions import _get_random, _reindex, generateNewId
from eea.workflow.readiness import ObjectReadiness
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class AggregatedEditPage(BrowserView):
    template = ViewPageTemplateFile('templates/assessment/aggregated_edit.pt')

    __call__ = template


class CreateVersion(BaseCreateVersion):
    """Create new version customizations for eea.versions """

    def __call__(self):
        version = create_version(self.context)
        return self.request.RESPONSE.redirect(version.absolute_url())


def create_version(original, request=None):
    """Creates a new version of an Assessment. Returns the new version object
    """
    pu = getToolByName(original, 'plone_utils')
    obj_uid = original.UID()
    obj_id = original.getId()
    obj_title = original.Title()
    obj_type = original.portal_type
    spec = parent(original)
    if request is None:
        request = original.REQUEST

    # Adapt version parent (if case)
    if not IVersionEnhanced.providedBy(original):
        alsoProvides(original, IVersionEnhanced)
    verparent = IVersionControl(original)
    verId = verparent.getVersionId()
    if not verId:
        verId = _get_random(10)
        verparent.setVersionId(verId)
        _reindex(original)

    # Create version object
    cp = spec.manage_copyObjects(ids=[obj_id])
    res = spec.manage_pasteObjects(cp)
    new_id = res[0]['new_id']

    ver = getattr(spec, new_id)

    # Remove copy_of from ID
    id = ver.getId()
    new_id = id.replace('copy_of_', '')
    new_id = generateNewId(spec, new_id, ver.UID())
    spec.manage_renameObject(id=id, new_id=new_id)

    # Set effective date today
    ver.setEffectiveDate(DateTime())

    # All the EEAFigures contained inside are copy of the ones in the previous assessment
    # but must be linked as new versions of the figures in the older assessment.
    # To achieve this, we must recreate all assessment parts and figures

    assessment = ver
    assessment.manage_delObjects(ids=ver.objectIds('AssessmentPart'))

    for pq in spec.objectValues('PolicyQuestion'):

        id = assessment.invokeFactory(type_name="AssessmentPart",
                id=assessment.generateUniqueId("AssessmentPart"),)
        ap = assessment[id]
        ap.setRelatedItems(pq)

        figures = get_figures_for_pq_in_assessment(pq, original)
        #now create versions of figures
        for fig in figures:
            version = base_create_version(fig)
            _parent = fig.aq_parent
            cp = _parent.manage_cutObjects(ids=[version.getId()])
            res = ap.manage_pasteObjects(cp)

        ap.reindexObject()

    # Set new state
    ver.reindexObject()
    original.reindexObject()    # _reindex(original)  #some indexed values of the context may depend on versions

    return ver

def get_figures_for_pq_in_assessment(pq, assessment):
    """Given a PolicyQuestion from a Specification and an Assessment, returns all EEAFigures
    contained in the AssessmentPart that answers to that PolicyQuestion"""

    path = pq.getPhysicalPath()

    assessment_part = None
    for part in assessment.objectValues('AssessmentPart'):
        pq = part.getRelatedItems()
        if pq:
            pq = pq[0]
        else:
            continue

        if pq.getPhysicalPath() == path:
            assessment_part = part
            break

    if assessment_part is not None:
        return assessment_part.objectValues('EEAFigure')

    return []


class WorkflowStateReadiness(ObjectReadiness):

    def field_has_value(self, fieldname, context):
        convert = getToolByName(self.context, 'portal_transforms').convert
        value = context.schema[fieldname].getAccessor(context)()
        return convert('html_to_text', value).getData()

    def is_ready_for(self, state_name):
        if state_name == 'published':
            #check that all the questions are answered
            ap = self.context.objectValues("AssessmentPart")
            missing = [p for p in ap if not self.field_has_value('assessment', p)]
            if missing:
                return False
            #check that the parent Specification is published
            parent = self.context.aq_parent
            wftool = getToolByName('portal_workflow')
            state = wftool.getInfoFor(parent, 'review_state')
            if state != "published":
                return False
            return True
        else:
            return super(WorkflowStateReadiness, self).is_ready_for(state_name)
