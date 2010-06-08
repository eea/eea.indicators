from zope.interface import implements
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView
from zope.publisher.interfaces import NotFound
from Products.CMFCore.utils import getToolByName
from valentine.imagescales.browser.interfaces import IImageView


class ImageViewAssessment(BrowserView):
    """ Get cover image from related EEAFigure of its AssessmentParts
    """
    implements(IImageView)

    def __init__(self, context, request):
        wftool = getToolByName(self.context, 'portal_workflow')

        super(ImageViewAssessment, self).__init__(context, request)

        # AssP of the main Q -> first publiched/draft related eeafigure
          #if none, get First AssP and its first published/draft eeafigure

        eeafile = None
        assessments = self.context.get_assessments()
        assessments_list = []
        assessments_list.append(assessments['key'])
        assessments_list.extend(assessments['secondary'])

        for assessment in assessments_list:
            for rel_ob in assessment.relatedItems():
                if rel_ob.portal_type == 'EEAFigure':
                    state = wftool.getInfoFor(rel_ob, 'review_state', '(Unknown)')
                    if state in ['published', 'visible']:
                        eeafile = rel_ob
                        break

        #TODO: check if eeafile has thumb
        self.img = queryMultiAdapter((eeafile, request), name=u'imgview')

    def display(self, scalename='thumb'):
        if not self.img:
            return False
        return self.img.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.display(scalename):
            return self.img(scalename)
        raise NotFound(self.request, scalename)
