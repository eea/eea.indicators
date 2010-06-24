from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.indicators.browser.interfaces import IIndicatorsPermissionsOverview
from eea.indicators.config import MANAGER_ROLE
from zope.interface import implements


class IndicatorsPermissionsOverview(BrowserView):
    implements(IIndicatorsPermissionsOverview)

    template = ViewPageTemplateFile('templates/permissions_overview.pt')

    __call__ = template

    def get_users_map(self):
        #pm = getToolByName(self.context, 'portal_membership')
        specs = self.context.objectValues("Specification")

        users = {}
        for spec in specs:
            specid, title = spec.getId(), spec.Title()
            roles = spec.computeRoleMap()
            for role in roles:
                userid = role['id']
                if role['local']:
                    for local in role['local']:
                        info = [{'role':role['local'], 
                                'specid':specid, 
                                'spectitle':title}]
                        #there's no defaultdict on python2.4
                        users[userid] = users.get(userid, []) + info

        return users

    def get_specs_map(self):
        specs = self.context.objectValues("Specification")

        specsmap = {}
        for spec in specs:
            key = (specid, title) = spec.getId(), spec.Title()
            roles = spec.computeRoleMap()
            for role in roles:
                userid = role['id']
                if role['local']:
                    for local in role['local']:
                        info = [{'userid':userid,
                                'role':local,
                                }]
                        specsmap[key] = specsmap.get(key, []) + info

        return specsmap

    def get_setcodes_map(self):
        #TODO: sort the results according to the code part of the setcode

        result = {}
        specs = self.context.objectValues("Specification")
        wftool = getToolByName(self.context, 'portal_workflow')

        for spec in specs:
            sets = [s['set'] for s in spec.getCodes()] 
            roles = spec.computeRoleMap()

            userids = []

            for role in roles:
                if MANAGER_ROLE in role['local']:
                    userids.append(role['id'])

            for s in sets:
                info = {
                        'spec':spec,
                        'userids':userids,
                        'role':MANAGER_ROLE,
                        'rolemap':roles,
                        'state':wftool.getInfoFor(spec, 'review_state', '(Unknown)'),
                        }
                if s in result.keys():
                    result[s].append(info)
                else:
                    result[s] = [info]

        return result
