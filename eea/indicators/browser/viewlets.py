""" Custom viewlets
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from plone.app.layout.viewlets import common


class AssessmentTopicsViewlet(common.ViewletBase):
    """ Assessment Topics field Viewlet
    """
    render = ViewPageTemplateFile('templates/viewlets/topics.pt')

    @property
    def available(self):
        """ Condition for rendering of this viewlets
        """
        plone = getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')
        return plone.is_view_template() and \
               self.context.portal_type == 'Assessment'


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


class AssessmentGeographicalCoverageViewlet(common.ViewletBase):
    """ Assessment GeographicalCoverage field Viewlet
    """
    render = ViewPageTemplateFile('templates/viewlets/geographical_coverage.pt')

    @property
    def available(self):
        """ Condition for rendering of this viewlets
        """
        plone = getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')
        return plone.is_view_template() and \
               self.context.portal_type == 'Assessment'


class AssessmentTemporalCoverageViewlet(common.ViewletBase):
    """ Assessment TemporalCoverage field Viewlet
    """
    render = ViewPageTemplateFile('templates/viewlets/temporal_coverage.pt')

    @property
    def available(self):
        """ Condition for rendering of this viewlets
        """
        plone = getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')
        return plone.is_view_template() and \
               self.context.portal_type == 'Assessment'