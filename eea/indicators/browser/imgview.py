""" Views to get images for indicators and assessments
"""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from eea.depiction.browser.interfaces import IImageView
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import NotFound


class ImageViewAssessment(BrowserView):
    """ Get cover image from related EEAFigure of its AssessmentParts
    """
    implements(IImageView)
    _img = False

    @property
    def img(self):
        """ self.img
        """
        if self._img is False:
            wftool = getToolByName(self.context, 'portal_workflow')
            assessments = self.context.get_assessments()
            assessments_list = []
            assessments_list.append(assessments['key'])
            assessments_list.extend(assessments['secondary'])

            eeafile = None
            for assessment in assessments_list:
                if not assessment:
                    continue
                for rel_ob in assessment.getRelatedItems():
                    if rel_ob.portal_type in (
                        'EEAFigure', 'DavizVisualization'):
                        state = wftool.getInfoFor(rel_ob,
                                                'review_state',
                                                '(Unknown)')
                        if state in ['published', 'visible']:
                            eeafile = rel_ob
                            break
            self._img = queryMultiAdapter(
                (eeafile, self.request), name=u'imgview')
        return self._img

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
    _img = False

    @property
    def img(self):
        """ self.img
        """
        if self._img is False:
            wftool = getToolByName(self.context, 'portal_workflow')
            eeafile = None
            for rel_ob in self.context.getRelatedItems():
                if not rel_ob:
                    continue
                if rel_ob.portal_type in ('EEAFigure', 'DavizVisualization'):
                    state = wftool.getInfoFor(rel_ob, 'review_state', '(Unknown)')
                    if state in ['published', 'visible']:
                        eeafile = rel_ob
                        break
            self._img = queryMultiAdapter((eeafile, self.request), name=u'imgview')
        return self._img

    def display(self, scalename='thumb'):
        """ display """
        if not self.img:
            return False
        return self.img.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.display(scalename):
            return self.img(scalename)
        raise NotFound(self.request, scalename)
