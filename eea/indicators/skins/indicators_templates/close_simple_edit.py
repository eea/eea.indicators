field = context.REQUEST.form.get('specific_field')
if not field:
    raise ValueError('We need a specific field here')

#value = context.schema[field].getAccessor(context)()
#<div id="value_response">%s</div> % value

return """
<script>
closer('%s');
</script>
""" % field 
