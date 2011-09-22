"""Integration with eea.themescentre
"""

from Acquisition import aq_inner, aq_parent
from eea.themecentre.interfaces import IThemeTagging

class AssessmentThemes(object):
    """Overrides the IThemeTagging adaptor for Assessments"""

    def __init__(self, context):
        """Constructor"""

        self.context = context
        self.parent = aq_parent(aq_inner(self.context))

    @property
    def tags(self):
        """ use the parent tags """
        return IThemeTagging(self.parent).tags

    @tags.setter
    def tags(self, value):
        """ do nothing on set"""
        pass

    @property
    def nondeprecated_tags(self):
        """ use the parent tags """
        return IThemeTagging(self.parent).nondeprecated_tags

    @nondeprecated_tags.setter
    def nondeprecated_tags(self, value):
        """ do nothing on set"""
        pass
