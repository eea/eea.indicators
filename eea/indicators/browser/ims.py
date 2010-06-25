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

