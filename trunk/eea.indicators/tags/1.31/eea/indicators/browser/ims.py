""" ims.py """

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


#TODO: write test for this sorting
def _get_code(set):
    """Usable as key in a comparision function"""
    def _wrapped(info):
        """cook function"""
        spec = info['spec']
        codes = get_codes(spec.get_codes)
        for code in codes:
            if set == code['set']:
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
        #TODO: rewrite this code so that it uses a map that's initialized
        #      with the spec > children

        #checks if spec id is in assessment path segments
        return filter(
                lambda b:spec.id == b.getPath().split('/')[-2],
                self.assessments
            )


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

            sets = [s['set'] for s in get_codes(spec.get_codes)]
            if not sets:
                sets = [None]

            for s in sets:
                info = {
                        'spec':spec,
                        'manager_id':self._get_name(spec),
                        'state':spec.review_state,
                        'assessments':assessments,
                        }
                if s in result.keys():
                    result[s].append(info)
                else:
                    result[s] = [info]

        for fs in self.factsheets:
            sets = [s['set'] for s in get_codes(fs.get_codes)]
            if not sets:
                sets = [None]

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

        for spec in self.specs:
            assessments = self.get_child_assessments(spec)
            for setcode in get_codes(spec.get_codes):
                set, code = setcode['set'], setcode['code']
                if not set in result:
                    result[set] = {}

                if not code in result[set]:
                    result[set][code] = {}

                d, p = self._get_instance_info(spec)
                year = d.year()

                result[set][code][year] = result[set][code].get(year, []) + \
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

                    result[set][code][year] = result[set][code].get(year, []) \
                          + [{
                              'type':'a',
                              'url':a.getURL(),
                              'state':p,
                              'title':a.Title,
                              'comments':a.comments,
                              'readiness':a.published_readiness}]

        for fs in self.factsheets:
            for setcode in get_codes(fs.get_codes):
                set, code = setcode['set'], setcode['code']
                if not set in result:
                    result[set] = {}

                if not code in result[set]:
                    result[set][code] = {}

                d, p = self._get_instance_info(fs)
                year = d.year()
                if year < earliest_year:
                    earliest_year = year
                if year > latest_year:
                    latest_year = year
                    if earliest_year == 0:
                        earliest_year = year

                result[set][code][year] = result[set][code].get(year, [])  + \
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

        return filter(lambda a:hasWrongVersionId(a.getObject()), assessments)


class ReportWrongVersionSpecifications(BrowserView):
    """ ReportWrongVersionSpecifications """

    def wrongs(self):
        """returns wrong specifications"""
        objs = self.context.objectValues(['Specification'])

        wrongs = filter(lambda o:o.has_duplicated_code(), objs)
        return wrongs


class ReportWrongMainCodeSpecifications(BrowserView):
    """ ReportWrongMainCodeSpecifications """

    def wrongs(self):
        """returns wrong specifications"""
        objs = self.context.objectValues(['Specification'])
        wrongs = filter(lambda o:bool(o.get_diff_vers_setcode()), objs)
        return wrongs

