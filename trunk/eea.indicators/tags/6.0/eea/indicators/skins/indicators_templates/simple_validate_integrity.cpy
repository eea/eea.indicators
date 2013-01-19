## Script (Python) "simple_validate_integrity"
##title=Validate Integrity
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##

#this is probably not needed
specific_field = context.REQUEST.form.get('specific_field')
state.set(specific_field=specific_field)
active_region = context.REQUEST.form.get('active_region')
if active_region:
	state.set(active_region=active_region)

errors = {}
errors = context.simple_validate(REQUEST=context.REQUEST, errors=errors)

if errors:
    return state.set(status='failure', errors=errors, portal_status_message='Please correct the indicated errors.')
else:
    return state.set(status='success', portal_status_message='Changes saved.')

