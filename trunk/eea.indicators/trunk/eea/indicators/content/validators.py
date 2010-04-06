# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

from Products.validation import validation
from Products.CMFPlone.utils import getToolByName
from Products.validation.interfaces.IValidator import IValidator


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
        if len(brains):
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
        query = {'portal_type': 'PolicyDocumentReference',
                 'getUrl': value}
        brains = cat(**query)
        if len(brains):
            for brain in brains:
                obj = brain.getObject()
                if kwargs['instance'].UID() != obj.UID():
                    return ("Validation failed, there is already an Policy Document pointing to this URL.")
        return 1

validation.register(UniquePolicyDocUrlValidator('unique_policy_url_validator'))