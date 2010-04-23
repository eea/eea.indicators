field = context.REQUEST.form.get('specific_field')
if not field:
    raise ValueError('We need a specific field here')
value = context.schema[field].getAccessor(context)()

return """
<div id="value_response">%s</div>
<script>
closer('%s');
</script>
""" % (value, field)
