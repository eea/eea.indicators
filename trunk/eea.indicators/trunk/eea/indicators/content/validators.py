# -*- coding: utf-8 -*-

"""Validators for eea.indicators content
"""

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Tiberiu Ichim"""

from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.UnicodeSplitter import process_unicode
from Products.CMFPlone.utils import getToolByName
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements


class UniquePolicyDocTitleValidator:
    """Validator"""

    implements(IValidator)

    def __init__(self,
                 name,
                 title='Unique Policy Document title',
                 description='Unique Policy Document title validator'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        words = process_unicode(unicode(value, 'utf-8'))
        cat = getToolByName(kwargs['instance'], 'portal_catalog')
        query = {'portal_type': 'PolicyDocumentReference',
                 'Title': list(words)}
        oid = kwargs['instance'].UID()
        brains = [b for b in cat(**query)
                  if (b.Title == value and b.getObject().UID() != oid)]

        if brains:
            return ("Validation failed, there is already an Policy "
                    "Document with this title.")

        return True

class UniquePolicyDocUrlValidator:
    """Validator"""
    implements(IValidator)

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
            if value == obj.getRemoteUrl() and \
              kwargs['instance'].UID() != obj.UID():
                return ("Validation failed, there is already an "
                        "Policy Document pointing to this URL.")
        return True

class OneAssessmentPartPerQuestionValidator:
    """ Validator """
    implements(IValidator)

    def __init__(self,
                 name,
                 title='One Assessment per Question',
                 description="Check if the PolicyQuestion is already answered"):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        instance = kwargs['instance']
        #catalog = getToolByName(instance, 'uid_catalog')
        #brains = catalog.searchResults(UID=value[0])

        path = instance.getPhysicalPath()

        for ap in aq_parent(aq_inner(instance)).objectValues('AssessmentPart'):
            if ap.getPhysicalPath() == path:    #same object
                continue

        return True


class FrequencyUpdateValidator:
    """Validates the frequency_years of frequency_of_updates
    """
    implements(IValidator)

    def __init__(self,
                 name,
                 title='Frequency in years validity',
                 description="Check if the frequency in years is valid"):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        # error message is required in order to trigger the validation
        error_msg = "Validation failed, Year value should be a number between" \
                    " 1 and 10"
        if not value and isinstance(value, basestring):
            return error_msg

        if isinstance(value, basestring): 
            if not value.strip():
                return error_msg
            if not value.isdigit():
                return error_msg
        frequency = value.get('frequency')
        if frequency:
            for row in frequency[0]:
                # skip row if there is no time_of_year which means it's empty
                if not row['time_of_year'].strip():
                    continue
                try:
                    v = int(row.get('years_freq'))
                except (TypeError, ValueError):
                    return error_msg

                if v not in range(1, 10):
                    return error_msg

        return True


class TimeOfYearValidator:
    """Validates the time_of_year of frequency_of_updates
    """
    implements(IValidator)

    def __init__(self,
                 name,
                 title='Time of year',
                 description="Check if the trimester is valid"):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if not value and isinstance(value, basestring):
            return False

        if value in ["Q1", "Q2", "Q3", "Q4"]:
            return True

        return False
