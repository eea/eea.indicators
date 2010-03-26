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
    template = ViewPageTemplateFile('templates/specification_view.pt')

    __call__ = template


class AggregatedEditPage(BrowserView):
    template = ViewPageTemplateFile('templates/specification_aggregated_edit.pt')

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
        obj_uid = self.context.UID()
        obj_id = self.context.getId()
        obj_title = self.context.Title()
        obj_type = self.context.portal_type
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
        #TODO: customize copy logic
        cp = parent.manage_copyObjects(ids=[obj_id])
        res = parent.manage_pasteObjects(cp)
        new_id = res[0]['new_id']

        ver = getattr(parent, new_id)

        # Remove copy_of from ID
        id = ver.getId()
        new_id = id.replace('copy_of_', '')
        new_id = self.generateNewId(parent, new_id, ver.UID())
        parent.manage_renameObject(id=id, new_id=new_id)

        # Set effective date today
        ver.setEffectiveDate(DateTime())

        # Set new state
        ver.reindexObject()
        _reindex(self.context)  #some indexed values of the context may depend on versions

        return self.request.RESPONSE.redirect(ver.absolute_url())
