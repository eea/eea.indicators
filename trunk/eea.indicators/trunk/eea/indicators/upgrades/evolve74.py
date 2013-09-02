""" Change storage of frequency_of_updates after the introduction of
a DataGridField widget
"""

from Products.CMFPlone.utils import getToolByName
import logging

logger = logging.getLogger('eea.indicators.migration')


def evolve(context):
    """ Migrate frequency_of_updates storage
    """

    catalog = getToolByName(context, 'portal_catalog')

    logger.info("Started migration of frequency_of_updates "
                "storage for Specifications")

    for b in catalog.searchResults(portal_type='Specification'):
        obj = b.getObject()
        field = obj.getField('frequency_of_updates')
        accessor = field.getEditAccessor(obj)
        value = accessor()
        freq_years = value.pop('frequency_years')
        freq_time_of_year = value.pop('time_of_year')


        if freq_years:
            frequency = [{'years_freq':freq_years, 
                          'time_of_year':freq_time_of_year},]
        else:
            frequency = []

        value['frequency'] = frequency
        field.set(obj, value)
        logger.info("Migrated frequency_of_updates storage for %s", 
                     obj.absolute_url())

