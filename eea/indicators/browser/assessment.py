from Acquisition import aq_base, aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import parent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import CreateVersion as BaseCreateVersion, create_version as base_create_version
from eea.versions.versions import _get_random, _reindex, generateNewId, get_versions_api
from eea.workflow.readiness import ObjectReadiness
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class IndexPage(BrowserView):
    """The Assessment index page"""


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

    #we want all Assessments for all spec versions to have the
    #same version id.
    #if the parent Specification has versions, then the Assessment
    #needs to be a version of those assessments

    parent_as = spec.objectValues('Assessment')
    ast = parent_as[0]  #NOTE: we rely on the oldest assessment being first
    version_id = IVersionControl(ast).versionId

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
    ver.setEffectiveDate(None)
    ver.setCreationDate(DateTime())

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
    IVersionControl(ver).setVersionId(version_id)   #setting the version ID to the assessments group version id
    ver.reindexObject()
    original.reindexObject()    # _reindex(original)  #some indexed values of the context may depend on versions

    return ver


class WorkflowStateReadiness(ObjectReadiness):
    """ObjectReadiness customizations"""

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
            parent = aq_parent(aq_inner(self.context))
            wftool = getToolByName(self.context, 'portal_workflow')
            state = wftool.getInfoFor(parent, 'review_state')
            if state != "published":
                return False
            return True
        else:
            return super(WorkflowStateReadiness, self).is_ready_for(state_name)

    def get_info_for(self, state_name):
        info = ObjectReadiness.get_info_for(self, state_name)
        #TODO: translate messages

        #TODO: add the required fields and info from the assessment parts
        ap = self.context.objectValues("AssessmentPart")
        
        missing = [p for p in ap if not self.field_has_value('assessment', p)]
        if missing:
            info['extra'].append(('error', 'You need to fill in the assessments for all the policy questions'))

        #check that the parent Specification is published
        parent = aq_parent(aq_inner(self.context))
        wftool = getToolByName(self.context, 'portal_workflow')
        state = wftool.getInfoFor(parent, 'review_state')
        if state != "published":
            info['extra'].append(('error', 'The parent Specification needs to be published'))

        return info


#def get_figures_for_pq_in_assessment(pq, assessment):
#    """Given a PolicyQuestion from a Specification and an Assessment, returns all EEAFigures
#    contained in the AssessmentPart that answers to that PolicyQuestion"""
#
#    path = pq.getPhysicalPath()
#
#    assessment_part = None
#    for part in assessment.objectValues('AssessmentPart'):
#        related = part.getRelatedItems()
#        pq = filter(lambda x:x.meta_type=='PolicyQuestion', related)
#        if pq:
#            pq = pq[0]
#        else:
#            continue
#
#        if pq.getPhysicalPath() == path:
#            assessment_part = part
#            break
#
#    if assessment_part is not None:
#        related = assessment_part.getRelatedItems()
#        figures = filter(lambda x:x.meta_type=='EEAFigure', related)
#        return figures
#
#    return []
