"""A mixin class for objects that function as indicators"""

import logging
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
#from eea.versions.versions import get_versions_api
from eea.versions.interfaces import IGetVersions
from Missing import Value as MissingValue

logger = logging.getLogger("eea.indicators.content")

class IndicatorMixin(object):
    """A mixin for Specification and IndicatorFactSheet"""

    security = ClassSecurityInfo()

    security.declarePublic("has_duplicated_code")
    def has_duplicated_code(self):
        """Return True if this specification has the wrong version id"""
        duplicates = self.get_duplicated_codes()
        return bool(duplicates)

    security.declarePublic("get_duplicated_codes")
    def get_duplicated_codes(self):
        """Returns codes that are duplicated by some other indicator"""

        versions = [v.UID() for v in IGetVersions(self).versions()]

        search = getToolByName(self, 'portal_catalog').searchResults
        codes = self.getCodes()
        self_UID = self.UID()

        #We want to see if there are other specs with the same code
        #that are not versions of this object.
        #if any version has the same UID as the checked object,
        #then we consider all versions to be the same as the object

        duplicated_codes = []
        for code in codes:
            code = code['set'] + code['code']
            brains = search(portal_type="Specification", get_codes=[code])
            #brains += cat(portal_type="IndicatorFactSheet", get_codes=[code])

            not_same = [b for b in brains if (b.UID not in versions)
                                         and (b.UID != self_UID)]

            # now we filter the specification based on their versionId;
            # we don't want to report all specifications in the versionId group
            _d = {}
            for b in not_same:
                if b.getVersionId == MissingValue: #this is infrequent
                    logger.warn( "Missing versionid value: %s", b.getObject())
                    continue
                _d[b.getVersionId.strip()] = b

            if _d:
                duplicated_codes.append((code, _d.values()))

        return duplicated_codes

    security.declarePublic("get_diff_vers_setcode")
    def get_diff_vers_setcode(self):
        """Returns a list of versions of this Spec that have
           a different main setcode
        """
        diff = []
        codes = self.getCodes()
        if not codes:
            return diff

        code = codes[0]
        for v in IGetVersions(self).versions():
            if v.getCodes() and v.getCodes()[0] != code:
                diff.append(v)
        return diff

    security.declarePublic('getCandidateFixedCode')
    def getCandidateFixedCode(self, spec):
        """Returns codes that a spec should get to have a similar main
           setcode to context
        """
        main = self.getCodes()[0]
        other = spec.getCodes()

        return [main] + [c for c in other if c != main]

    security.declarePublic('format_codes')
    def format_codes(self, codes):
        """format codes"""
        return ", ".join(["%s%s" % (s['set'], s['code']) for s in codes])
