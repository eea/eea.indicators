# -*- coding: utf-8 -*-

""" Views for IMS v1 content migrated to v3
"""

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class FiguresForAlbum(BrowserView):
    """ Return related EEAFigures as brains for atct_album_view display
    """

    def __call__(self):
        cat = getToolByName(self.context, 'portal_catalog')
        figures = []
        uids = []

        for rel_ob in self.context.getRelatedItems():
            if rel_ob.portal_type == 'EEAFigure':
                figures.append(rel_ob)

        uids = [fig_ob.UID() for fig_ob in figures]
        query = {'UID': uids, 'review_state':'published'}
        brains = [b for b in cat.searchResults(query)]
        return brains

class KeyMessages(BrowserView):
    """ Return contained KeyMessage objects
    """

    def __call__(self):
        return self.context.getFolderContents(contentFilter={
                    'portal_type': 'KeyMessage',
                    'review_state': ['published'],
               }, full_objects = True)

class FactSheetDocuments(BrowserView):
    """ Return contained FactSheetDocument objects
    """

    def __call__(self):
        return self.context.getFolderContents(contentFilter={
                    'portal_type': 'FactSheetDocument',
                    'review_state': ['published'],
               }, full_objects = True)
