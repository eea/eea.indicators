## Script (Python) "indicators_get_referer"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##

if not REQUEST:
    REQUEST = context.REQUEST

path = REQUEST.HTTP_REFERER

path = path.replace(context.portal_url(), '', 1)

path = path.split('/')

if not path[0]:
    path = path[1:]

if 'edit' in path[-1]:
    path = path[:-1]

path = '/'.join(path)

try:
    referer = context.restrictedTraverse(path)
except Exception:
    return ''

if getattr(referer, 'portal_type', '') == 'Assessment':
    return '/www/SITE/' + referer.aq_parent.absolute_url(1)
elif getattr(referer, 'portal_type', '') == 'AssessmentPart':
    return '/www/SITE/' + referer.aq_parent.aq_parent.absolute_url(1)
else:
    return ''
