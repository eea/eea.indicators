# -*- coding: utf-8 -*-
""" Specification controllers
"""

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Tiberiu Ichim"""

from DateTime import DateTime
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZPublisher.Client import querify
from eea.indicators.browser.utils import has_one_of
from eea.versions.interfaces import IVersionControl
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import assign_version as base_assign_version
from eea.versions.versions import create_version as base_create_version
from eea.versions.versions import _random_id
from eea.versions.interfaces import IGetVersions
from eea.workflow.interfaces import IFieldIsRequiredForState, IValueProvider
from eea.workflow.readiness import ObjectReadiness
from plone.app.layout.globals.interfaces import IViewView
from zope.component import getMultiAdapter
from zope.interface import implements
import logging
#from zope.interface import alsoProvides

logger = logging.getLogger('eea.indicators.browser.specification')


class IndexPage(BrowserView):
    """ Index page """

    def getId(self):
        return "view"


class AggregatedEditPage(BrowserView):
    """Agg edit page"""
    implements(IViewView)

    template = \
        ViewPageTemplateFile('templates/specification/aggregated_edit.pt')

    __call__ = template


class SchemataCounts(BrowserView):
    """Provides a dictionary of fields that are required for publishing
    grouped by schematas

    ZZZ: see if able/worthy to move this to eea.workflow
    """

    def __call__(self):
        schematas = {}
        for field in self.context.schema.fields():
            if not field.schemata in schematas:
                schematas[field.schemata] = []
            req = getMultiAdapter((self.context, field),
                    IFieldIsRequiredForState)('published')
            if req:
                adapter = getMultiAdapter((self.context, field), IValueProvider)
                if not adapter.has_value():
                    schematas[field.schemata].append(field.__name__)

        return schematas


class AssessmentVersions(BrowserView):
    """ Return contained Assessments divided by 'published' and 'draft' sorted
        by publish_date and creation_date
    """

    def __call__(self):
        res = {'published': [], 'draft': []}

        get = lambda o:o.effective_date or o.creation_date

        assessments = self.context.getFolderContents(
                             contentFilter={'review_state':'published',
                                            'portal_type':'Assessment'},
                             full_objects = True)
        res['published'] = list(reversed(sorted(assessments, key=get)))

        assessments = self.context.getFolderContents(
                             contentFilter={'review_state':'draft',
                                            'portal_type':'Assessment'},
                             full_objects = True)

        res['draft'] = list(reversed(sorted(assessments, key=get)))

        return res


def create_version(original, request=None):
    """ Create version
    """
    new_spec = base_create_version(original, False)
    new_spec.setEffectiveDate(None)

    #Delete assessments and work items
    new_spec.manage_delObjects(ids=new_spec.objectIds('Assessment'))
    new_spec.manage_delObjects(ids=new_spec.objectIds('WorkItem'))

    #ZZZ: should we reindex the objects here?
    for obj in new_spec.objectValues():
        obj.setEffectiveDate(None)
        obj.setCreationDate(DateTime())

    new_spec.reindexObject()
    original.reindexObject() #some indexed values of the context may
                             #depend on versions
    return new_spec


class CreateVersion(BaseCreateVersion):
    """Create new version customizations for eea.versions """

    def __call__(self):
        new = self.create()
        return self.request.RESPONSE.redirect(new.absolute_url())

    def create(self):
        """ create version"""
        new = create_version(self.context)
        return new


class WorkflowStateReadiness(ObjectReadiness):
    """Overrides default readiness adapter"""

    #ZZZ: translate messages here
    checks = {'published':(
            (
                lambda o: not has_one_of(('Data', 'ExternalDataSpec'),
                                            o.getRelatedItems()),
                "You need to point to at least one EEA Data or ExternalData"),
            (
                lambda o:not bool(o.objectValues("PolicyQuestion")),
                "You need to add at least one Policy Question"),
            (
                lambda o: not bool([x for x in o.objectValues('PolicyQuestion') 
                                    if x.getIs_key_question()]),
                "At least one PolicyQuestion needs to be main policy question"),
            (
                lambda o:not bool(o.getThemes()),
                "You need to specify one primary theme" ),
            (
                lambda o:o.has_duplicated_code(),
                "The <a href='#rfs_codes'>Indicator Specification code</a> is "
                "already used by some other document in IMS"),
            )}


class PolicyQuestions(BrowserView):
    """ Return contained PolicyQuestions divided by 'is_key_question' property
    """

    def __call__(self):
        res = {'all': [], 'key_questions': [], 'questions': []}

        questions = self.context.getFolderContents(
                           contentFilter={'portal_type':'PolicyQuestion'},
                           full_objects = True)

        res['all'] = questions
        for question in questions:
            if question.getIs_key_question():
                res['key_questions'].append(question)
            else:
                res['questions'].append(question)

        return res


class ContactInfo(BrowserView):
    """ Return LDAP user based on manager_user_id
    """

    def __call__(self):
        manager_id = self.context.getManager_user_id()
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.getMemberInfo(manager_id)


def get_assessment_vid_for_spec_vid(context, versionid):
    """Returns an assessment version id

    Given a version id for a specification, returns the version id of the
    assessments that are contained in any of the Specifications from that
    versioning group.
    """

    vid = _random_id(context, 10)
    cat = getToolByName(context, 'portal_catalog')
    p = '/'.join(context.getPhysicalPath())
    brains = cat.searchResults({'getVersionId':versionid,
                                'portal_type':'Specification'})
    brains = [b for b in brains if b.getPath() != p]

    for brain in brains:
        obj = brain.getObject()
        children = obj.objectValues('Assessment')
        if children:
            vid = IGetVersions(children[0]).versionId
            break

    return vid


def spec_assign_version(context, new_version):
    """Assign a specific version id to an object

    We override the same method from eea.versions. We want to
    be able to reassign version for children Assessments to be
    at the same version as the children Assessments of the target
    Specification version.

    Also, we want to assign the new version to all specification
    that had the old version.
    """

    #assign new version to context
    base_assign_version(context, new_version)

    #search for specifications with the old version and assign new version
    other_assessments = []  #optimization: children assessments from other specs
    versions = [o for o in IGetVersions(context).versions()
                           if o.meta_type == "Specification"]
    for o in versions:
        IVersionControl(o).setVersionId(new_version)
        o.reindexObject()
        other_assessments.extend(o.objectValues("Assessment"))

    #reassign version ids to context assessments + assessments
    #from related specifications
    vid = get_assessment_vid_for_spec_vid(context, new_version)
    for asmt in (list(context.objectValues('Assessment')) +
                 list(other_assessments)):
        IVersionControl(asmt).setVersionId(vid)
        asmt.reindexObject()


class AssignVersion(object):
    """ Assign new version ID
    """

    def __call__(self):
        pu = getToolByName(self.context, 'plone_utils')
        new_version = self.request.form.get('new-version', '')
        nextURL = self.request.form.get('nextURL', self.context.absolute_url())

        if new_version:
            spec_assign_version(self.context, new_version)
            message = _(u'Version ID changed.')
        else:
            message = _(u'Please specify a valid Version ID.')

        pu.addPortalMessage(message, 'structure')
        return self.request.RESPONSE.redirect(nextURL)


class WrongVersionReport(BrowserView):
    """Reports what's wrong with the current version id of a specification"""

    def current_version(self):
        """current version"""
        return IGetVersions(self.context).versionId

    def get_duplicated_codes(self):
        """gets duplicated codes"""
        return self.context.get_duplicated_codes()


class SetCodes(BrowserView):
    """Set codes view"""

    def __call__(self):
        #this is a list of form ['APE', '009', 'CSI', '001', 'CLIM', '003']
        codes = self.request.form.get("codes")

        value = [{'set':setc, 'code':code}
                    for setc, code in zip(codes[::2], codes[1::2])]

        field = self.context.schema['codes']
        field.getStorage(self.context).set(field.getName(), self.context, value)
        return "Fixed"


class FragmentFrequencyOfUpdatesView(BrowserView):
    """View for fragment_frequency_of_updatesik
    """


class FragmentMetadataView(BrowserView):
    """View for fragment_metadata
    """

    schematas = ['categorization', 'dates', 'ownership', 'settings']
    exclude = ['relatedItems', 'location']   #'location',  'subject'

    def field_names(self):
        """ field names
        """
        c = self.context
        fields = c.schema.filterFields(lambda f:f.schemata in self.schematas)
        fields = [f.getName() for f in fields if f.getName() not 
                                                        in self.exclude]

        return fields

    def fields(self):
        """returns a query for fields
        """
        return querify([('fields', self.field_names())])
