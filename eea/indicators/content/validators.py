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


class UniquePolicyDocTitleValidator(object):
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
                  if b.Title == value and b.getObject().UID() != oid]

        if brains:
            return ("Validation failed, there is already an Policy "
                    "Document with this title.")

        return True

class UniquePolicyDocUrlValidator(object):
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

class OneAssessmentPartPerQuestionValidator(object):
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


class FrequencyUpdateValidator(object):
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
                val = row.get('years_freq')
                if not val:
                    continue
                try:
                    v = int(val)
                except (TypeError, ValueError):
                    return error_msg

                if v not in range(1, 10):
                    return error_msg

        return True


class TimeOfYearValidator(object):
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


class CodesValidator(object):
    """Validates the codes number
    """
    implements(IValidator)

    def __init__(self,
                 name,
                 title='Code number',
                 description="Check if the code is valid"):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if not value and isinstance(value, basestring):
            return False

        instance = kwargs['instance']
        cat = getToolByName(instance, 'portal_catalog')
        for val in value:
            val_code = int(val.get('code') or 0, base=10)
            val_set = val.get('set')
            val_id_code = '%s%d' % (val_set, val_code)
            res = cat(get_codes=val_set, sort_on='created', sort_order='reverse',
                      sort_limit=1)
            if not res:
                return True
            res_codes = res[0].get_codes
            code_value = 0
            for code in res_codes:
                if val_set in code:
                    if len(val_set) < len(code):
                        code_value = int(code.split(val_set)[-1], base=10)
                        break
            if val_code == code_value:
                clim_obj = res[0].getObject()
                versions_view = clim_obj.restrictedTraverse('@@getVersions', '')
                if versions_view:
                    versions = versions_view.versions()
                    found_version = False
                    for version in versions:
                        if instance == version or instance == version.aq_parent:
                            found_version = True
                            break
                    if not found_version:
                        return ("Validation failed, you can only use the code "
                                "%s if related to %s" %
                                (val_id_code, versions[0].absolute_url()))
            if val_code < code_value:
                return ("Validation failed, code for %s cannot be lower "
                        "then 0%d" % (val_set, code_value))
        return False
