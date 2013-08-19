""" Upgrades
"""

from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import getToolByName
from eea.versions.interfaces import IVersionEnhanced
from zope.interface import alsoProvides, providedBy
import logging
import transaction


logger = logging.getLogger('eea.indicators.migration')


def assign_iversionenhanced_to_content(gstool):
    """ Update IMS content to provide IVersionEnhanced if they should
    """
    portal = getToolByName(gstool, 'portal_url').getPortalObject()

    catalog = portal.portal_catalog

    ctypes = ['Specification', 'Assessment', 'IndicatorFactSheet']

    for _type in ctypes:
        res = catalog.searchResults(portal_type=_type)
        for brain in res:
            obj = brain.getObject()
            if shasattr(obj, '__annotations__'):
                if 'versionId' in obj.__annotations__.keys():
                    if not IVersionEnhanced in providedBy(obj):
                        alsoProvides(obj, IVersionEnhanced)
                        logger.info(u"Added IVersionEnhanced to %s", obj)


def cleanup_assessmentparts(gstool):
    """ Cleanup AssessmentPart annotation that contains missing daviz info
    """
    portal = getToolByName(gstool, 'portal_url').getPortalObject()

    catalog = portal.portal_catalog
    res = catalog.searchResults(portal_type='AssessmentPart')
    uids_cat = getToolByName(portal, 'uid_catalog')

    logger.info("Starting cleanup of assessmentpart-daviz annotation")
    i = 0
    for b in res:
        obj = b.getObject()
        annot = obj.__annotations__.get('DAVIZ_CHARTS', {})

        for uid in annot.keys():
            brains = uids_cat.searchResults(UID=uid)
            if not brains:
                msg = "Couldn't find object for brain with UID %s, "\
                      "deleting from assessmentpart %s" % (uid,
                      obj.absolute_url())
                logger.info(msg)
                del annot[uid]
                annot._p_changed = True
                obj._p_changed = True
                i += 1
                continue

            daviz = brains[0].getObject()
            if daviz is None:   #brain does not lead to object?
                msg = "Couldn't find object for brain with UID %s, "\
                      "deleting from assessmentpart %s" % (uid,
                      obj.absolute_url())
                logger.info(msg)
                del annot[uid]
                annot._p_changed = True
                obj._p_changed = True
                i += 1

        if (i % 20) == 0:
            transaction.savepoint() #savepoint on every 20 changes

    transaction.commit()

    logger.info("End cleanup of assessmentpart-daviz annotation")
