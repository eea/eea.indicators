""" Manager
"""
from plone.app.portlets.manager import ColumnPortletManagerRenderer

class IndicatorsPortletManagerRenderer(ColumnPortletManagerRenderer):
    """Indicators specific renderer for portlet managers.
    """
    def portletsToShow(self):
        """ Visible portlets
        """
        portlets = []
        for p in self.allPortlets():
            if p['available']:
                if p['name'] == 'readiness':
                    portlets.insert(0, p)
                else:
                    portlets.append(p)
        return portlets
