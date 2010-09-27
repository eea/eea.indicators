from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.browser.interfaces import IIndicatorsPermissionsOverview
from zope.interface import implements
import DateTime
import re


#TODO: write test for this sorting
def _get_code(set):
    def _wrapped(info):
        spec = info['spec']
        codes = spec.getCodes()
        for code in codes:
            if set == code['set']:
                return code['code']

        return None
    return _wrapped


class IndicatorsOverview(BrowserView):
    implements(IIndicatorsPermissionsOverview)

    template = ViewPageTemplateFile('templates/ims_overview.pt')

    __call__ = template
    def _get_name(self, spec):
        user = spec.getManager_user_id()
        info = self.mtool.getMemberInfo(user)
        if info:
            return info.get('fullname', user)
        return user

    def get_setcodes_map(self):

        result = {}
        specs = self.context.objectValues("Specification")

        wftool = getToolByName(self.context, 'portal_workflow')
        self.mtool = mtool = getToolByName(self.context, 'portal_membership')

        get_state = lambda a:wftool.getWorkflowsFor(a)[0].states[wftool.getInfoFor(a, 'review_state', '(Unknown)')].title

        for spec in specs:
            sets = [s['set'] for s in spec.getCodes()]
            if not sets:
                sets = [None]
            assessments = [(a, get_state(a)) for a in spec.objectValues("Assessment")]

            for s in sets:
                info = {
                        'spec':spec,
                        'manager_id':self._get_name(spec),
                        'state':get_state(spec),
                        'assessments':assessments,
                        }
                if s in result.keys():
                    result[s].append(info)
                else:
                    result[s] = [info]

        for k, v in result.items():
            v.sort(key=_get_code(k))

        return result

    def codeset_for(self, codes, setname):
        codesets = [code for code in codes if code['set'] == setname]
        if codesets:
            codeset = codesets[0]
        else:
            codeset = {'set':'', 'code':''}

        return codeset


codesre = re.compile(r"([a-zA-Z]+)(\d+)")

class IndicatorsTimeline(BrowserView):
    """Presents a timeline based structure for Assessments
    """

    def get_codes(self, codes):
        res = []
        for code in codes:
            match = codesre.match(code)
            if match:
                res.append(match.groups())
        return res

    def get_child_assessments(self, spec):
        #checks if spec id is in assessment path segments
        #TODO: test if changing the self.assessments list by deleting those found results in faster code
        return filter(
                lambda b:spec.id in b.getPath().split('/'),
                self.assessments)

    def _get_instance_info(self, instance):
        d = instance.EffectiveDate
        if d and d != 'None' and not isinstance(d, tuple):
            p = 'published'
            d = DateTime.DateTime(d)
        else:
            p = 'pending'
            d = DateTime.DateTime(instance.CreationDate)

        return d, p

    def get_timeline(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        self.specs = catalog.searchResults(portal_type='Specification')
        self.assessments = catalog.searchResults(portal_type='Assessment')

        result = {
                #example of data structure:
                #'TERM':{
                #    '001':{
                #        '1999':[('a', href)], #assessment at link href
                #        'published':('p', href),    #assessment in Publication href
                #        }
                #    }
                }

        earliest_year = 0
        latest_year = 0

        for i, spec in enumerate(self.specs):
            assessments = self.get_child_assessments(spec)
            for set, code in self.get_codes(spec.get_codes):
                if not set in result:
                    result[set] = {}

                if not code in result[set]:
                    result[set][code] = {}

                d, p = self._get_instance_info(spec)
                year = d.year()

                #comments = len(spec.getReplyReplies(spec))
                #readiness = IObjectReadiness(spec).get_info_for('published')['rfs_done']

                result[set][code][year] = result[set][code].get(year, [])  + \
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
                    #comments = len(a.getReplyReplies(a))
                    #readiness = IObjectReadiness(a).get_info_for('published')['rfs_done']

                    result[set][code][year] = result[set][code].get(year, []) + \
                          [{
                              'type':'a', 
                              'url':a.getURL(), 
                              'state':p, 
                              'title':a.Title, 
                              'comments':a.comments, 
                              'readiness':a.published_readiness}]

            if i > 10:
                break
        return ((earliest_year, latest_year), result)
