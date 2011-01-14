# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Tiberiu Ichim"""

from DateTime import DateTime
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.browser.utils import has_one_of
from eea.indicators.content.Specification import assign_version
from eea.versions.versions import CreateVersion as BaseCreateVersion
from eea.versions.versions import create_version as base_create_version
from eea.workflow.interfaces import IFieldIsRequiredForState, IValueProvider
from eea.workflow.readiness import ObjectReadiness
from zope.component import getMultiAdapter

import logging
logger = logging.getLogger('eea.indicators')


class IndexPage(BrowserView):
    """ Index page """


class AggregatedEditPage(BrowserView):
    """Agg edit page"""
    template = \
        ViewPageTemplateFile('templates/specification/aggregated_edit.pt')

    __call__ = template


class SchemataCounts(BrowserView):
    """Provides a dictionary of fields that are required for publishing 
    grouped by schematas

    TODO: see if able/worthy to move this to eea.workflow
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
    new_spec = base_create_version(original, False)
    new_spec.setEffectiveDate(None)

    #Delete assessments and work items
    new_spec.manage_delObjects(ids=new_spec.objectIds('Assessment'))
    new_spec.manage_delObjects(ids=new_spec.objectIds('WorkItem'))

    #TODO: should we reindex the objects here?
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
        new = create_version(self.context)
        return self.request.RESPONSE.redirect(new.absolute_url())


class WorkflowStateReadiness(ObjectReadiness):
    """Overrides default readiness adapter"""

    #TODO: translate messages here
    checks = {'published':(
            (
                lambda o: not has_one_of(('Data', 'ExternalDataSpec'), 
                                            o.getRelatedItems()),
                "You need to point to at least one EEA Data or ExternalData"),
            (
                lambda o:not bool(o.objectValues("PolicyQuestion")),
                "You need to add at least one Policy Question"),
            (
                lambda o:not filter(lambda x:x.getIs_key_question(), 
                                    o.objectValues('PolicyQuestion')),
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


class AssignVersion(object):
    """ Assign new version ID
    """

    def __call__(self):
        pu = getToolByName(self.context, 'plone_utils')
        new_version = self.request.form.get('new-version', '')
        nextURL = self.request.form.get('nextURL', self.context.absolute_url())

        if new_version:
            assign_version(self.context, new_version)
            message = _(u'Version ID changed.')
        else:
            message = _(u'Please specify a valid Version ID.')

        pu.addPortalMessage(message, 'structure')
        return self.request.RESPONSE.redirect(nextURL)


class WrongVersionReport(BrowserView):
    """Reports what's wrong with the current version id of a specification"""

    def current_version(self):
        """current version"""
        return get_version_id(self.context)

    def get_duplicated_codes(self):
        """gets duplicated codes"""
        return self.context.get_duplicated_codes()


class SetCodes(BrowserView):
    """Set codes view"""

    def __call__(self):
        #this is a list of form ['APE', '009', 'CSI', '001', 'CLIM', '003']
        codes = self.request.form.get("codes")  

        value = [{'set':set, 'code':code} 
                    for set, code in zip(codes[::2], codes[1::2])]

        field = self.context.schema['codes']
        field.getStorage(self.context).set(field.getName(), self.context, value)
        return "Fixed"

