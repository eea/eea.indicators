""" eea.indicators 8.7 migration scripts
"""
import transaction

from Products.CMFPlone.utils import getToolByName
import logging
from eea.indicators.content.utils import set_location

logger = logging.getLogger('eea.indicators.migration')


def evolve(context):
    """ Migrate locations for Assessments
    """

    catalog = getToolByName(context, 'portal_catalog')

    logger.info("Started setting of location for Assessment")
    res = catalog.searchResults(portal_type='Assessment')
    total = len(res)
    count = 0
    for b in res:
        try:
            obj = b.getObject()
        except Exception:
            logger.error("Can't retrieve object %s", b.getURL(1))
            continue
        logger.info("Set location from relations for %s", obj.absolute_url())
        set_location(obj)
        count += 1
        if count % 100 == 0:
            transaction.commit()
            logger.info('INFO: Subtransaction committed to zodb (%s/%s)', count,
                     total)

    logger.info("Ending setting of location for Assessment")
