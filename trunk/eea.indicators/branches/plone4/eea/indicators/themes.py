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

    def _get_tags(self):
        return IThemeTagging(self.parent).tags

    def _set_tags(self, value):
        """ do nothing on set"""
        pass

    tags = property(_get_tags, _set_tags)

    def _get_nondeprecated_tags(self):
        """ use the parent tags """
        return IThemeTagging(self.parent).nondeprecated_tags

    def _set_nondeprecated_tags(self):
        """ do nothing on set"""
        pass

    nondeprecated_tags = property(_get_nondeprecated_tags, 
                                  _set_nondeprecated_tags)


    #@property
    #def tags(self):
        #""" use the parent tags """
        #return IThemeTagging(self.parent).tags

    #@tags.setter
    #def tags(self, value):
        #""" do nothing on set"""
        #pass

    #@property
    #def nondeprecated_tags(self):
        #""" use the parent tags """
        #return IThemeTagging(self.parent).nondeprecated_tags

    #@nondeprecated_tags.setter
    #def nondeprecated_tags(self, value):
        #""" do nothing on set"""
        #pass
