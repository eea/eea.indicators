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
        versions = getMultiAdapter((context, request), name='getVersions')()
        cat = getToolByName(kwargs['instance'], 'portal_catalog')

        field = context.schema['codes']
        value = get_dgf_value(field, value)
        codes = ["".join((v['set'], v['code'])) for v in value]

        for code in codes:
            # {'query':codes,'operator':'or'}
            brains = cat(portal_type='Specification', get_codes=[code])

            #first, check if the spec is the same as the one being edited
            brains = [b for b in brains if b.id != spec_id]
            if brains:
                return ("Validation failed, there is already another Specification with code %s" % code)

            #next, check if the objects are versions of the instance
            objs = [b.getObject() for b in brains]

        return True

validation.register(UniqueSpecificationCode('unique_specification_code'))
