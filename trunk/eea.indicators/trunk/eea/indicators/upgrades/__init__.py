""" Upgrades
"""

from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import getToolByName
from eea.versions.interfaces import IVersionEnhanced
from zope.interface import alsoProvides, providedBy

import logging
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
                        logger.info(u"Added IVersionEnhanced to %s" % obj)

