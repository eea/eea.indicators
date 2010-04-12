from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.content.Specification import required_for_publication
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import _get_random, _reindex
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy


class IndexPage(BrowserView):
    template = ViewPageTemplateFile('templates/specification/view.pt')

    __call__ = template


class AggregatedEditPage(BrowserView):
    template = ViewPageTemplateFile('templates/specification/aggregated_edit.pt')

    __call__ = template


class SchemataCounts(BrowserView):
    """Provides a dictionary of fields that are required for publishing grouped by schematas
    
    
    TODO: see if able to move this to eea.workflow
    """

    def __call__(self):
        fields = required_for_publication

        schematas = {}
        for field in self.context.schema.fields():
            if not field.schemata in schematas:
                schematas[field.schemata] = []
            req = getattr(field, 'required_for_published', False)
            if req:
                #TODO: text fields should be stripped of HTML to see if they really have content
                if not field.getAccessor(self.context)():  #we assume that the value return is something not empty
                    schematas[field.schemata].append(field.__name__)

        return schematas


class CreateVersion(BaseCreateVersion):
    """Create new version customizations for eea.versions """

    def __call__(self):
        pu = getToolByName(self.context, 'plone_utils')
        #obj_uid = self.context.UID()
        obj_id = self.context.getId()
        #obj_title = self.context.Title()
        #obj_type = self.context.portal_type
        parent = utils.parent(self.context)

        # Adapt version parent (if case)
        if not IVersionEnhanced.providedBy(self.context):
            alsoProvides(self.context, IVersionEnhanced)
        verparent = IVersionControl(self.context)
        verId = verparent.getVersionId()
        if not verId:
            verId = _get_random(10)
            verparent.setVersionId(verId)
            _reindex(self.context)

        # Create version object
        clipb = parent.manage_copyObjects(ids=[obj_id])
        res = parent.manage_pasteObjects(clipb)
        new_id = res[0]['new_id']

        ver = getattr(parent, new_id)

        # Fixes the generated id: remove copy_of from ID
        #TODO: add -vX sufix to the ids
        id = ver.getId()
        new_id = id.replace('copy_of_', '')
        new_id = self.generateNewId(parent, new_id, ver.UID())
        parent.manage_renameObject(id=id, new_id=new_id)
        new_spec = parent[new_id]

        # Set effective date today
        ver.setEffectiveDate(DateTime())

        #Delete assessments and work items
        for id in new_spec.objectIds('Assessment'):
            new_spec._delOb(id) #shouldn't send IObjectRemovedEvent

        for id in new_spec.objectIds('WorkItem'):
            new_spec._delOb(id)


        # Set new state
        ver.reindexObject()
        _reindex(self.context)  #some indexed values of the context may depend on versions

        return self.request.RESPONSE.redirect(ver.absolute_url())
