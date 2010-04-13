from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import _get_random, _reindex
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy


class AggregatedEditPage(BrowserView):
    template = ViewPageTemplateFile('templates/assessment/aggregated_edit.pt')

    __call__ = template


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
