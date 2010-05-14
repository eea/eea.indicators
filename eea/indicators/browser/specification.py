# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Tiberiu Ichim"""

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.content.Specification import required_for_publication
from eea.versions.interfaces import IVersionControl, IVersionEnhanced
from eea.versions.versions import CreateVersion as BaseCreateVersion, generateNewId
from eea.versions.versions import _get_random, _reindex
from eea.workflow.readiness import ObjectReadiness
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy

import logging
logger = logging.getLogger('eea.indicators')

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
        fields = required_for_publication   #TODO: rename this to required_for_published

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

    #TODO: take out duplicate code that is now found in
    #eea.versions.versions.create_version

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
        new_id = generateNewId(parent, new_id, ver.UID())
        parent.manage_renameObject(id=id, new_id=new_id)
        new_spec = parent[new_id]

        # Set effective date today
        ver.setEffectiveDate(DateTime())

        #Delete assessments and work items
        #new_spec._delOb(id) #shouldn't send IObjectRemovedEvent
        new_spec.manage_delObjects(ids=new_spec.objectIds('Assessment'))
        new_spec.manage_delObjects(ids=new_spec.objectIds('WorkItem'))


        # Set new state
        ver.reindexObject()
        _reindex(self.context)  #some indexed values of the context may depend on versions

        return self.request.RESPONSE.redirect(ver.absolute_url())


class WorkflowStateReadiness(ObjectReadiness):
    def is_ready_for(self, state_name):
        if state_name == 'published':
            #check if there's at least one reference to a DataSpec
            #TODO: this checks for relationship to ExternalDataSpec
            #when the ExternalDataSpec + EEADATA is unified, check that this works
            if not self.context.getRelatedItems():
                return False

            #check if there's at least one main policy question
            pq = self.context.objectValues("PolicyQuestion")
            mains = [q for q in pq if q.getIs_key_question() == True]
            if not mains:
                return False

            return True
        else:
            return super(WorkflowStateReadiness, self).is_ready_for(state_name)

class AssessmentVersions(BrowserView):
    """ Return contained Assessments divided by 'published' and 'draft' sorted
        by publish_date and creation_date
    """

    def sort_assessments(self, data):
        """ """
        wftool = getToolByName(self.context, 'portal_workflow')
        assessments = {}

        for assessment in data:
            try:
                info = wftool.getStatusOf('indicators_workflow', assessment)
                time = info['time']
                assessments[time] = assessment
            except Exception, err:
                logger.exception('Exception: %s ', err)

        res = assessments.keys()
        res.sort()

        return [assessments[k] for k in res]

    def __call__(self):
        res = {'published': [], 'draft': []}

        assessments = self.context.getFolderContents(
                             contentFilter={'review_state':'published',
                                            'portal_type':'Assessment'},
                             full_objects = True)
        res['published'] = self.sort_assessments(assessments)

        assessments = self.context.getFolderContents(
                             contentFilter={'review_state':'draft',
                                            'portal_type':'Assessment'},
                             full_objects = True)
        res['draft'] = self.sort_assessments(assessments)

        return res

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
        manager_ob = None
        manager_id = self.context.getManager_user_id()

        # Get LDAP user
        try:
            #TODO: #3292
            manager_ob = self.context.acl_users.EIONETLDAPNEW.acl_users.getUser(manager_id)
        except Exception, err:
            logger.exception('Exception: %s ', err)

        return manager_ob

