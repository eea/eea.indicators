from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import _get_random, _reindex, generateNewId
from zope.interface import alsoProvides


class AggregatedEditPage(BrowserView):
    template = ViewPageTemplateFile('templates/assessment/aggregated_edit.pt')

    __call__ = template


class CreateVersion(BaseCreateVersion):
    """Create new version customizations for eea.versions """

    def __call__(self):
        version = create_version(self.context)
        return self.request.RESPONSE.redirect(version.absolute_url())


def create_version(original):
    """Creates a new version of an Assessment. Returns the new version object
    """
    pu = getToolByName(original, 'plone_utils')
    obj_uid = original.UID()
    obj_id = original.getId()
    obj_title = original.Title()
    obj_type = original.portal_type
    parent = utils.parent(original)

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
    #TODO: customize copy logic
    cp = parent.manage_copyObjects(ids=[obj_id])
    res = parent.manage_pasteObjects(cp)
    new_id = res[0]['new_id']

    ver = getattr(parent, new_id)

    # Remove copy_of from ID
    id = ver.getId()
    new_id = id.replace('copy_of_', '')
    new_id = generateNewId(parent, new_id, ver.UID())
    parent.manage_renameObject(id=id, new_id=new_id)

    # Set effective date today
    ver.setEffectiveDate(DateTime())

    # Set new state
    ver.reindexObject()
    _reindex(original)  #some indexed values of the context may depend on versions

    return ver
