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

    #def tags():
    #    """The tags"""

    def gett(self):
        """ use the parent tags """
        return IThemeTagging(self.parent).tags

    def sett(self, value):
        """ do nothing on set"""
        pass

    tags = property(gett, sett)

    def get_nondeprecated_tags(self):
        """ use the parent tags """
        return IThemeTagging(self.parent).nondeprecated_tags

    def set_nondeprecated_tags(self, value):
        """ do nothing on set"""
        pass

    nondeprecated_tags = property(get_nondeprecated_tags, set_nondeprecated_tags)
