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

    def get_setcodes_map(self):

        result = {}
        specs = self.context.objectValues("Specification")

        wftool = getToolByName(self.context, 'portal_workflow')
        get_state = lambda a:wftool.getInfoFor(a, 'review_state', '(Unknown)')

        for spec in specs:
            sets = [s['set'] for s in spec.getCodes()] 
            if not sets:
                sets = [None]
            assessments = [(a, get_state(a)) for a in spec.objectValues("Assessment")]

            for s in sets:
                info = {
                        'spec':spec,
                        'manager_id':spec.getManager_user_id(),
                        'state':wftool.getInfoFor(spec, 'review_state', '(Unknown)'),
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
        specs = self.context.objectValues("Specification")
        wftool = getToolByName(self.context, 'portal_workflow')
        get_state = lambda a:wftool.getInfoFor(a, 'review_state', '(Unknown)')

        result = {
                #example of data structure:
                #'TERM':{
                #    '001':{
                #        '1998':[('n', None)], #no specification for that year
                #        '1999':[('a', href)], #assessment at link href
                #        'published':('p', href),    #assessment in Publication href
                #        'future':[('f', href)],    #assessment has no effective date
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
                    result[set][code] = {'future':[],}

                if not assessments:
                    #TODO: see if there's a related EEAPublication to the Specification
                    #pseudocode
                    #if published(a):
                    #    result[set][code]['p'] = [(p, p.absolute_url())]
                    result[set][code]['missing'] = [('m', spec.absolute_url())].extend(result[set][code].get('missing', []))

                for a in assessments:
                    d = a.getEffectiveDate()
                    if not d:
                        print "adding a for future", a
                        result[set][code]['future'] = [('f', a.absolute_url())].extend(result[set][code].get('future'))
                        continue
                    year = d.year()
                    if year < earliest_year:
                        earliest_year = year
                    if year > latest_year:
                        latest_year = year
                        if earliest_year == 0:
                            earliest_year = year

                    #TODO: use .append to return lists instead of overriding. 
                    result[set][code][year] = [('a', a.absolute_url()),]

        return ((earliest_year, latest_year), result)
