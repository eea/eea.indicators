from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

def get_dgf_value(field, value):
    """Cleanup the value returned for a DataGridField from a form post """

    #code adapted from DataGridField code
    column_ids = field.getColumnIds()
    cleaned = []
    doSort = False

    for row in value:
        order = row.get('orderindex_', None)
        
        empty = True
                        
        if order != "template_row_marker":
            # don't process hidden template row as
            # input data                     
            
            val = {}
            for col in column_ids:
                val[col] = (row.get(col,'')).strip()
                
                if val[col] != '':
                    empty = False
                                                                
            if order is not None:                        
                try:
                    order = int(order)
                    doSort = True
                except ValueError:
                    pass

            # create sortable tuples
            if (not field.allow_empty_rows) and empty:
                pass
            else:
                cleaned.append((order, val.copy()))

    if doSort:
        cleaned.sort()

    # remove order keys when sorting is complete
    value = tuple([x for (throwaway, x) in cleaned])
    value = [v for v in value if (v['set'] and v['code'])]  #make sure set+code are entered

    return value

def get_specific_parent(startobj, criteria):
    """Finds a specific parent for the startobj

    Criteria is a callable. For example:
    >>> criteria = lambda o: ISpecification.providedBy(o)

    If nothing is found, raise ValueError
    """ 

    parent = startobj
    find = None
    while not criteria(parent):
        try:
            parent = parent.aq_parent
        except AttributeError:
            raise ValueError
        if IPloneSiteRoot.providedBy(parent):
            raise ValueError

    if criteria(parent): #doublecheck just to make sure
        find = parent

    if find is None:
        raise ValueError

    return find
