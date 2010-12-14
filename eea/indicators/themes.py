"""Integration with eea.themescentre 
"""

from Acquisition import aq_inner, aq_parent
from eea.themecentre.interfaces import IThemeTagging


class AssessmentThemes(object):
    """Overrides the IThemeTagging adaptor for Assessments"""

    def __init__(self, context):
        self.context = context
        self.parent = aq_parent(aq_inner(self.context))

    def tags():
        def get(self):
            return IThemeTagging(self.parent).tags

        def set(self, value):
            pass

        return property(get, set)
    tags = tags()

