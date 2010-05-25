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

