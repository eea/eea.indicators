from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.browser.interfaces import IIndicatorsPermissionsOverview
from zope.interface import implements


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


class IndicatorsTimeline(BrowserView):
    """Presents a timeline based structure for Assessments
    """

    def get_timeline(self):

        #PUBLISHED = 'published'

        specs = self.context.objectValues("Specification")
        wftool = getToolByName(self.context, 'portal_workflow')
        get_state = lambda a:wftool.getInfoFor(a, 'review_state', '(Unknown)')

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
        for spec in specs:
            assessments = spec.objectValues("Assessment")
            for codeset in spec.getCodes():
                set, code = codeset['set'], codeset['code']
                if not set in result:
                    result[set] = {}

                if not code in result[set]:
                    result[set][code] = {}  #'future':[],

#               if not assessments:
#                   #TODO: see if there's a related EEAPublication to the Specification
#                   #pseudocode
#                   #if published(a):
#                   #    result[set][code]['p'] = [(p, p.absolute_url())]
#                   #else:
#                   result[set][code]['missing'] = [('m', spec.absolute_url())] + result[set][code].get('missing', [])

                d = spec.getEffectiveDate()
                p = 'published'    #is published
                if not d:
                    d = spec.creation_date
                    p = 'pending'
                year = d.year()

                result[set][code][year] = result[set][code].get(year, [])  + [('s', spec.absolute_url(), p, spec.Title())]

                for a in assessments:
                    d = a.getEffectiveDate()
                    p = 'published'
                    if not d:
                        #assessment is not published
                        #result[set][code]['future'] = [('f', a.absolute_url())] + result[set][code].get('future', [])
                        d = a.creation_date
                        p = 'pending'
                    year = d.year()
                    if year < earliest_year:
                        earliest_year = year
                    if year > latest_year:
                        latest_year = year
                        if earliest_year == 0:
                            earliest_year = year

                    result[set][code][year] = result[set][code].get(year, []) + [('a', a.absolute_url(), p, a.Title())]

        return ((earliest_year, latest_year), result)
