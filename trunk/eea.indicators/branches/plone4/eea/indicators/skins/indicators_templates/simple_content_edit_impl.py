## Script (Python) "simple_content_edit_impl"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state, id=''
##

from Products.Archetypes import PloneMessageFactory as _
from Products.Archetypes.utils import addStatusMessage
from Products.CMFCore.utils import getToolByName

REQUEST = context.REQUEST
old_id = context.getId()

#this is probably not needed
specific_field = context.REQUEST.form.get('specific_field')
state.set(specific_field=specific_field)

try:
    new_context = context.portal_factory.doCreate(context, id)
except AttributeError:
    # Fallback for AT + plain CMF where we don't have a portal_factory
    new_context = context

new_context.simpleProcessForm(REQUEST=REQUEST)

# Get the current language and put it in request/LANGUAGE
form = REQUEST.form
if form.has_key('current_lang'):
    form['language'] = form.get('current_lang')

portal_status_message = _(u'Changes saved.')

fieldset = REQUEST.get('fieldset', None)
schemata = new_context.Schemata()

env = state.kwargs
reference_source_url = env.get('reference_source_url')
if reference_source_url is not None:
    reference_source_url = env['reference_source_url'].pop()
    reference_source_field = env['reference_source_field'].pop()
    reference_source_fieldset = env['reference_source_fieldset'].pop()
    portal = context.portal_url.getPortalObject()
    reference_obj = portal.restrictedTraverse(reference_source_url)

    portal_status_message = _(u'message_reference_added',
                              default=u'Reference added.')

    edited_reference_message = _(u'message_reference_edited',
                                 default=u'Reference edited.')

    # XXX disabled mark creation flag
    ## context.remove_creation_mark(old_id)

    kwargs = {
        'status':'success_add_reference',
        'context':reference_obj,
        'fieldset':reference_source_fieldset,
        'field':reference_source_field,
        'reference_focus':reference_source_field,
        }
    return state.set(**kwargs)

if state.errors:
    errors = state.errors
    s_items = [(s, schemata[s].keys()) for s in schemata.keys()]
    fields = []
    for s, f_names in s_items:
        for f_name in f_names:
            fields.append((s, f_name))
    for s_name, f_name in fields:
        if errors.has_key(f_name):
            REQUEST.set('fieldset', s_name)
            addStatusMessage(REQUEST, portal_status_message)
            return state.set(
                status='failure',
                context=new_context,)

if not state.errors:
    from Products.Archetypes.utils import transaction_note
    transaction_note('Edited %s %s at %s' % (new_context.meta_type,
                                             new_context.title_or_id(),
                                             new_context.absolute_url()))

addStatusMessage(REQUEST, portal_status_message)

return state.set(status='success',
                 context=new_context,
                 )

