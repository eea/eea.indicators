""" Views to get images for indicators and assessments
"""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from valentine.imagescales.browser.interfaces import IImageView
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import NotFound


class ImageViewAssessment(BrowserView):
    """ Get cover image from related EEAFigure of its AssessmentParts
    """
    implements(IImageView)

    def __init__(self, context, request):
        wftool = getToolByName(context, 'portal_workflow')

        super(ImageViewAssessment, self).__init__(context, request)

        eeafile = None
        assessments = context.get_assessments()
        assessments_list = []
        assessments_list.append(assessments['key'])
        assessments_list.extend(assessments['secondary'])

        for assessment in assessments_list:
            for rel_ob in assessment.getRelatedItems():
                if rel_ob.portal_type == 'EEAFigure':
                    state = wftool.getInfoFor(rel_ob,
                                              'review_state',
                                              '(Unknown)')
                    if state in ['published', 'visible']:
                        eeafile = rel_ob
                        break

        self.img = queryMultiAdapter((eeafile, request), name=u'imgview')

    def display(self, scalename='thumb'):
        """ display """
        if not self.img:
            return False
        return self.img.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.display(scalename):
            return self.img(scalename)
        raise NotFound(self.request, scalename)


class ImageViewIndicatorFactSheet(BrowserView):
    """ Get cover image from related EEAFigure
    """
    implements(IImageView)

    def __init__(self, context, request):
        wftool = getToolByName(context, 'portal_workflow')

        super(ImageViewIndicatorFactSheet, self).__init__(context, request)

        eeafile = None
        for rel_ob in context.getRelatedItems():
            if rel_ob.portal_type == 'EEAFigure':
                state = wftool.getInfoFor(rel_ob, 'review_state', '(Unknown)')
                if state in ['published', 'visible']:
                    eeafile = rel_ob
                    break

        self.img = queryMultiAdapter((eeafile, request), name=u'imgview')

    def display(self, scalename='thumb'):
        """ display """
        if not self.img:
            return False
        return self.img.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.display(scalename):
            return self.img(scalename)
        raise NotFound(self.request, scalename)
