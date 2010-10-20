field = context.REQUEST.form.get('specific_field')
active_region = context.REQUEST.form.get('active_region');

if not field:
    raise ValueError('We need a specific field here')

url = context.absolute_url() + '/edit_aggregated';

if active_region:
    return """
<script>
closer('%s', '%s', '%s');
</script>
""" % (field, active_region, url); 
else:
    return """
<script>
closer('%s', null, '%s');
</script>
""" % (field, url)
