## Script (Python) "simple_content_edit"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=''
##
return context.simple_content_edit_impl(state, id)
