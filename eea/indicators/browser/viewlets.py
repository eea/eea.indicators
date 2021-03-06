""" Custom viewlets
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from plone.app.layout.viewlets import common


class AssessmentDatesViewlet(common.ViewletBase):
    """ Assessment Dates field Viewlet
    """
    render = ViewPageTemplateFile('templates/viewlets/dates.pt')

    @property
    def available(self):
        """ Condition for rendering of this viewlets
        """
        plone = getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')

        return plone.is_view_template() and \
               self.context.portal_type == 'Assessment'
