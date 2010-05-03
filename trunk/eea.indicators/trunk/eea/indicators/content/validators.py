# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Tiberiu Ichim"""

from Products.CMFPlone.utils import getToolByName
from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from eea.indicators.content.utils import get_dgf_value
from zope.component import getMultiAdapter


class UniquePolicyDocTitleValidator:
    __implements__ = IValidator

    def __init__(self,
                 name,
                 title='Unique Policy Document title',
                 description='Unique Policy Document title validator'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        cat = getToolByName(kwargs['instance'], 'portal_catalog')
        query = {'portal_type': 'PolicyDocumentReference',
                 'Title': value}
        brains = cat(**query)
        for brain in brains:
            obj = brain.getObject()
            if kwargs['instance'].UID() != obj.UID():
                return ("Validation failed, there is already an Policy Document with this title.")
        return 1

validation.register(UniquePolicyDocTitleValidator('unique_policy_title_validator'))


class UniquePolicyDocUrlValidator:
    __implements__ = IValidator

    def __init__(self,
                 name,
                 title='Unique Policy Document URL',
                 description='Unique Policy Document URL validator'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        cat = getToolByName(kwargs['instance'], 'portal_catalog')
        query = {'portal_type': 'PolicyDocumentReference'}
        brains = cat(**query)
        for brain in brains:
            obj = brain.getObject()
            if value == obj.getRemoteUrl() and kwargs['instance'].UID() != obj.UID():
                return ("Validation failed, there is already an Policy Document pointing to this URL.")
        return 1

validation.register(UniquePolicyDocUrlValidator('unique_policy_url_validator'))


class UniqueSpecificationCode:
    __implements__ = IValidator

    def __init__(self,
                 name,
                 title='Unique Specification code',
                 description='Check if the Specification code already exists in IMS'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        context = kwargs['instance']
        request = kwargs['REQUEST']
        spec_id = context.getId()
        versions = getMultiAdapter((context, request), name='getVersions')().values()
        cat = getToolByName(kwargs['instance'], 'portal_catalog')

        field = context.schema['codes']
        value = get_dgf_value(field, value)

        #check if the codes are numeric
        not_numeric = []
        for row in value:
            code = row['code']
            try:
                code = int(code)
            except ValueError:
                not_numeric.append(row)
        if not_numeric:
            not_numeric = ", ".join(
                [
                    " ".join(
                            (row['set'], str(row['code']))
                            ) for row in not_numeric
                ]
            )
            return "Validation failed, you need to enter a number for set code(s): %s" % not_numeric

        codes = ["".join((v['set'], v['code'])) for v in value]

        for code in codes:
            #Now we check if there are other specifications in IMS that are not:
            #the same object or versions of the same object
            #To do this, we retrieve a list of all specifications with the same
            #code and we filter out those that are versions or identical objs

            brains = cat(portal_type='Specification', get_codes=[code])
            objs = [b.getObject() for b in brains]
            not_same = []
            for obj in objs:
                path = obj.getPhysicalPath()

                #if any version has the same path as the checked object,
                #then we consider all versions to be the same as the object
                if not [v for v in versions if v.getPhysicalPath() == path]:
                    not_same.append(obj)

            if not_same:
                return ("Validation failed, there is already another Specification with code %s" % code)

        return True


validation.register(UniqueSpecificationCode('unique_specification_code'))

class OneAssessmentPartPerQuestionValidator:
    __implements__ = IValidator

    def __init__(self,
                 name,
                 title='One Assessment per Question',
                 description="Check if the PolicyQuestion is already answered"):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        instance = kwargs['instance']
        catalog = getToolByName(instance, 'uid_catalog')
        brains = catalog.searchResults(UID=value[0])
        pq = brains[0].getObject()

        q_path = pq.getPhysicalPath()
        path = instance.getPhysicalPath()

        for ap in instance.aq_parent.objectValues('AssessmentPart'):
            if ap.getPhysicalPath() == path:    #same object
                continue
            if ap.getRelatedItems().getPhysicalPath() == q_path:
                return "Validation failed, there's already an Assessment Part that answers this question"

        return True

validation.register(OneAssessmentPartPerQuestionValidator('one_assessment_per_question'))
