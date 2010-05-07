field = context.REQUEST.form.get('specific_field')
active_region = context.REQUEST.form.get('active_region');

if not field:
    raise ValueError('We need a specific field here')

#value = context.schema[field].getAccessor(context)()
#<div id="value_response">%s</div> % value

if active_region:
    return """
<script>
closer('%s', '%s');
</script>
""" % (field, active_region); 
else:
    return """
<script>
closer('%s', null);
</script>
""" % field 
