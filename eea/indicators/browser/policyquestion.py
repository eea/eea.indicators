from Products.Five import BrowserView
from zope.component import queryAdapter

from eea.versions.interfaces import IGetVersions

class KeyMessages(BrowserView):
    """ search for the latest version of the first related item and return
    its key message to be displayed in the question view """

    def get_versions(self):
        related = [rel for rel in self.context.getBRefs('relatesTo')
                   if rel is not None]
        if related:
            related = related[0]
            return queryAdapter(related, IGetVersions)

    def get_assessment(self):
        versions = self.get_versions()
        if versions:
            return versions.latest_version()

    def key_messages(self):
        assessment = self.get_assessment()
        if assessment:
            return assessment.getKey_message()

    def assessment_url(self):
        versions = self.get_versions()
        if versions:
            return versions.getLatestVersionUrl()

    def assessment_date(self):
        versions = self.get_versions()
        if versions:
            return self.context.toLocalizedTime(
                self.get_assessment().effective())
