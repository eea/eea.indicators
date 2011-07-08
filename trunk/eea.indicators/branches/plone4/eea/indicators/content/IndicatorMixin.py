"""A mixin class for objects that function as indicators"""


from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from eea.versions.versions import get_versions_api
from Missing import Value as MissingValue


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

        versions = map(
                lambda v:'/'.join(v.getPhysicalPath()),
                get_versions_api(self).versions.values()
            )

        cat = getToolByName(self, 'portal_catalog')
        codes = self.getCodes()
        self_path = '/'.join(self.getPhysicalPath())

        #We want to see if there are other specs with the same code
        #that are not versions of this object.
        #if any version has the same path as the checked object,
        #then we consider all versions to be the same as the object

        duplicated_codes = []
        for code in codes:

            code = code['set'] + code['code']
            brains = cat(portal_type="Specification", get_codes=[code])
            #brains += cat(portal_type="IndicatorFactSheet", get_codes=[code])

            not_same = []
            for b in brains:
                p = b.getPath()
                if (p not in versions) and (p != self_path):
                    not_same.append(b)

            if not_same:
                d = []
                for b in not_same:
                    if not filter(lambda o:o.getPath() == b.getPath(), d):
                        d.append(b)
                _d = {}
                for b in d:
                    v = b.getVersionId.strip()
                    if v != MissingValue:
                        try:
                            _d[v] = b
                        except Exception, e:
                            import pdb; pdb.set_trace()
                    else:
                        print "Missing versionid value: ", b.getObject()
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
        for v in get_versions_api(self).versions.values():
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

        return [main] + list(filter(lambda c:c!=main, other))

    security.declarePublic('format_codes')
    def format_codes(self, codes):
        """format codes"""
        return ", ".join(["%s%s" % (s['set'], s['code']) for s in codes])
