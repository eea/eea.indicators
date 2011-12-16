""" Traversing utilities
"""

from eea.indicators.content.interfaces import ISpecification
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements
from zope.traversing.interfaces import ITraversable
from zope.traversing.adapters import DefaultTraversable

#from Products.Five.traversable import FiveTraversable

ANNO_MARKER = '__ims_migration__'

class SpecificationTraverser(DefaultTraversable):   #FiveTraversable
    """ traversal adapter to get an assessment based on its
        old ID after the migration from ims.eionet.europa.eu
    """
    implements(ITraversable)
    adapts(ISpecification)

    def fallback(self, name, furtherPath):
        """ fallback method """
        return super(SpecificationTraverser, self).traverse(name, furtherPath)

    def traverse(self, name, furtherPath):
        """ traverse method """
        context = self._subject

        if name.startswith('IAssessment'):
            assessments = context.objectValues('Assessment')
            for assessment in assessments:
                anno = IAnnotations(assessment)
                anno_url = anno.get(ANNO_MARKER)
                old_url = anno_url[ANNO_MARKER]
                if name in old_url:
                    return assessment

        return self.fallback(name, furtherPath)
