"""Autorelations for eea.indicators"""

from zope.component import getMultiAdapter


class LatestFigures(object):
    """ Return the latest figures from latest assessment for a specification.
    """
    def __init__(self, context):
        """Constructor"""
        self.context = context
        self.request = getattr(self.context, 'REQUEST', None)

    def __call__(self, **kwargs):
        """ Return all the related data sets from the assessments figures.
        """

        #get my published assessments
        assessments = getMultiAdapter((self.context, self.request),
                                   name=u'assessment_versions')
        all_assessments = assessments()
        published_assessments = all_assessments['published']
        if len(published_assessments) > 0 :
            latest_assessment = published_assessments[0]
        else:
            latest_assessment = None

        #get the figures for each assessment part, we can use related_items view
        figs = []
        if latest_assessment:
            #take the key part
            part = latest_assessment.objectValues('AssessmentPart')[-1]
            related_items = getMultiAdapter((part, self.request),
                                   name=u'related_items')
            figs = related_items('EEAFigure')

        return [('Latest figures', figs)]
