field = context.REQUEST.form.get('specific_field')
if not field:
    raise ValueError('We need a specific field here')

return """
<div id="value_response">%s</div>
<script>
closer('%s');
</script>
""" % (context.schema[field].getAccessor(context)(), field)
