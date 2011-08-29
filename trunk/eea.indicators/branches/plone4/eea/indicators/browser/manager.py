from zope.interface import implements

from plone.portlets.interfaces import IPortletManagerRenderer
from plone.portlets.manager import PortletManagerRenderer

class IndicatorFactSheetPortletManagerRenderer(PortletManagerRenderer):
    """IndicatorFactSheet specific renderer for portlet managers.
    """

    def portletsToShow(self):
        print "new renderer"
        return [p for p in self.allPortlets() if p['available']]
