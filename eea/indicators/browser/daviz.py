"""Integration with eea.daviz
"""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from persistent.mapping import PersistentMapping
import urlparse


class SetDavizChart(BrowserView):
    """Edit the chart for a daviz presentation that's set as related
    """

    def __call__(self):
        uid = self.request.form.get("daviz_uid")
        chart = self.request.form.get("chart")
        if chart:
            selected_charts = urlparse.parse_qs(chart)['chart']
        else:
            selected_charts = []
        context_uid = self.request.form.get("context_uid")


        #looks like relatedItems-96797d03-1e39-432f-ae82-8c3eedcf2342-widget
        #obj_uid = context_uid[13:-7]
        #uids_cat = getToolByName(self.context, 'uid_catalog')
        #obj = uids_cat.searchResults(UID=obj_uid)[0].getObject()

        obj = self.context
        annot = IAnnotations(obj)
        
        if not 'DAVIZ_CHARTS' in annot:
            annot['DAVIZ_CHARTS'] = PersistentMapping()
        
        annot['DAVIZ_CHARTS'][uid.strip()] = selected_charts

        print obj, annot['DAVIZ_CHARTS'].items()
        
        return "done"
