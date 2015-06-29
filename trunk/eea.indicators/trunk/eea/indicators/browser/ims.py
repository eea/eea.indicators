""" ims.py """

from eea.versions.interfaces import IGetVersions
from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.browser.interfaces import IIndicatorsPermissionsOverview
from eea.indicators.content.Assessment import hasWrongVersionId
from zope.interface import implements
import DateTime
import re

codesre = re.compile(r"([a-zA-Z]+)(\d+)")

def get_codes(codes):
    """Extract real setcodes from codes in metadata format

    Splits a list such as ['CSI001', 'CSI', "TERM001", "TERM"] into
    tuples of form [('CSI', '001'), ('TERM', '001')]
    """

    res = []
    for code in codes:
        match = codesre.match(code)
        if match:
            g = match.groups()
            res.append({'set':g[0], 'code':g[1]})
    return res


#ZZZ: write test for this sorting
def _get_code(sets):
    """Usable as key in a comparision function"""
    def _wrapped(info):
        """cook function"""
        spec = info['spec']
        codes = get_codes(spec.get_codes)
        for code in codes:
            if sets == code['set']:
                return code['code']

        return None
    return _wrapped


class BaseIndicatorsReport(object):
    """ BaseIndicatorsReport """
    specifications = None
    assessments = None
    factsheets = None

    def get_child_assessments(self, spec):
        """Returns child assessments"""
        #ZZZ: rewrite this code so that it uses a map that's initialized
        #      with the spec > children

        #checks if spec id is in assessment path segments
        return [b for b in self.assessments
                if spec.id == b.getPath().split('/')[-2]]


class IndicatorsOverview(BrowserView, BaseIndicatorsReport):
    """ IndicatorsOverview """
    implements(IIndicatorsPermissionsOverview)

    template = ViewPageTemplateFile('templates/ims_overview.pt')

    __call__ = template

    def _get_name(self, spec):
        """get name"""
        user = spec.getObject().getManager_user_id()
        info = self.mtool.getMemberInfo(user)
        if info:
            return info.get('fullname', user)
        return user

    def get_setcodes_map(self):
        """get secodes map"""

        result = {}

        catalog = getToolByName(self.context, 'portal_catalog')
        self.specifications = catalog.searchResults(portal_type='Specification')
        self.assessments = catalog.searchResults(portal_type='Assessment')
        self.factsheets = catalog.searchResults(
                             portal_type='IndicatorFactSheet')

        self.mtool = getToolByName(self.context, 'portal_membership')

        for spec in self.specifications:
            assessments = [(a, a.review_state)
                           for a in self.get_child_assessments(spec)]

            sets = [s['set'] for s in get_codes(spec.get_codes)] or ["none"]

            for st in sets:
                info = {
                        'spec':spec,
                        'manager_id':self._get_name(spec),
                        'state':spec.review_state,
                        'assessments':assessments,
                        }
                if st in result.keys():
                    result[st].append(info)
                else:
                    result[st] = [info]

        for fs in self.factsheets:
            sets = [ms['set'] for ms in get_codes(fs.get_codes)] or ["none"]

            for s in sets:
                info = {
                        'spec':fs,
                        'manager_id':'',
                        'state':fs.review_state,
                        'assessments':[],
                        }
                if s in result.keys():
                    result[s].append(info)
                else:
                    result[s] = [info]

        for k, v in result.items():
            v.sort(key=_get_code(k))

        return result

    def codeset_for(self, codes, setname): #used by the view template
        """return codeset"""
        codes = get_codes(codes)

        codesets = [code for code in codes if code['set'] == setname]
        if codesets:
            codeset = codesets[0]
        else:
            codeset = {'set':'', 'code':''}

        return codeset


class IndicatorsTimeline(BrowserView, BaseIndicatorsReport):
    """Presents a timeline based structure for Assessments
    """

    def _get_instance_info(self, instance):
        """get instance info"""
        d = instance.EffectiveDate
        if d and d != 'None' and not isinstance(d, tuple):
            d = DateTime.DateTime(d)
        else:
            d = DateTime.DateTime(instance.CreationDate)

        return d, instance.review_state

    def get_timeline(self):
        """get timeline"""
        catalog = getToolByName(self.context, 'portal_catalog')
        self.specs = catalog.searchResults(portal_type='Specification')
        self.assessments = catalog.searchResults(portal_type='Assessment')
        self.factsheets = catalog.searchResults(
                               portal_type='IndicatorFactSheet')

        result = {
                #example of data structure:
                #'TERM':{
                #    '001':{
                #  '1999':[('a', href)], #assessment at link href
                #  'published':('p', href), #assessment in Publication href
                #        }
                #    }
                }

        earliest_year = 0
        latest_year = 0
        none = [{'set':"missing setcode", 'code':' '}]

        for spec in self.specs:
            assessments = self.get_child_assessments(spec)
            for setcode in get_codes(spec.get_codes) or none:
                setc, code = setcode['set'], setcode['code']
                if not setc in result:
                    result[setc] = {}

                if not code in result[setc]:
                    result[setc][code] = {}

                d, p = self._get_instance_info(spec)
                year = d.year()

                result[setc][code][year] = result[setc][code].get(year, []) + \
                        [{'type':'s',
                            'url':spec.getURL(),
                            'state':p,
                            'title':spec.Title,
                            'comments':spec.comments,
                            'readiness':spec.published_readiness}]

                for a in assessments:
                    d, p = self._get_instance_info(a)
                    year = d.year()
                    if year < earliest_year:
                        earliest_year = year
                    if year > latest_year:
                        latest_year = year
                        if earliest_year == 0:
                            earliest_year = year

                    result[setc][code][year] = result[setc][code].get(
                        year, []) + [{
                              'type': 'a',
                              'url': a.getURL(),
                              'state': p,
                              'title': a.Title,
                              'comments': a.comments,
                              'readiness': a.published_readiness}]

        for fs in self.factsheets:
            for setcode in get_codes(fs.get_codes) or none:
                setc, code = setcode['set'], setcode['code']
                if not setc in result:
                    result[setc] = {}

                if not code in result[setc]:
                    result[setc][code] = {}

                d, p = self._get_instance_info(fs)
                year = d.year()
                if year < earliest_year:
                    earliest_year = year
                if year > latest_year:
                    latest_year = year
                    if earliest_year == 0:
                        earliest_year = year

                result[setc][code][year] = result[setc][code].get(year, [])  + \
                        [{'type':'f',
                            'url':fs.getURL(),
                            'state':p,
                            'title':fs.Title,
                            'comments':fs.comments,
                            'readiness':100}]

        return ((earliest_year, latest_year), result)


class ReportWrongVersionAssessments(BrowserView):
    """ ReportWrongVersionAssessments """

    def wrongs(self):
        """returns wrong assessments"""
        catalog = getToolByName(self.context, 'portal_catalog')
        assessments = catalog.searchResults(portal_type='Assessment')

        return [a for a in assessments if hasWrongVersionId(a.getObject())]


class ReportWrongVersionSpecifications(BrowserView):
    """ ReportWrongVersionSpecifications """

    def wrongs(self):
        """returns wrong specifications"""
        objs = self.context.objectValues(['Specification'])
        return [o for o in objs if o.has_duplicated_code()]


class ReportWrongMainCodeSpecifications(BrowserView):
    """ ReportWrongMainCodeSpecifications """

    def wrongs(self):
        """returns wrong specifications"""
        objs = self.context.objectValues(['Specification'])
        return [o for o in objs if bool(o.get_diff_vers_setcode())]

#class ReadinessRenderer(Renderer):
    #render = ViewPageTemplateFile('templates/portlet_readiness.pt')

class IncludeJqueryUI(BrowserView):
    """ Include jQuery UI
    """
    def __call__(self):
        return True


class LatestAssessmentVersions(BrowserView):
    """Returns a list of urls for all latest assessments

    It needs to be called as anonymous to get the published
    latest versions.
    """
    def __call__(self):
        cat = self.context.portal_catalog
        brains = cat.searchResults(portal_type="Assessment",
                                   review_state="published")

        result = []

        for b in brains:
            o = b.getObject()
            latest = IGetVersions(o).latest_version()
            result.append(latest.absolute_url())

        result = sorted(list(set(result)))  #sort and keep only unique links

        links = ["%s/@@esms.xml" % l for l in result]

        return "\n".join(links)
