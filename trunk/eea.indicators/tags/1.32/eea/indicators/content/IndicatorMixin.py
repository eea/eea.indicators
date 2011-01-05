"""A mixin class for objects that function as indicators"""


from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from eea.versions.versions import get_versions_api


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
                    _d[b.getVersionId.strip()] = b
                duplicated_codes.append((code, _d.values()))

        return duplicated_codes
