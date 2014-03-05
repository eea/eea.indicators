"""Various utilities for content types
"""

from Acquisition import aq_inner, aq_parent
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
import json
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
                    doSort = False

            # create sortable tuples
            if (not field.allow_empty_rows) and empty:
                pass
            else:
                cleaned.append((order, val.copy()))

    if doSort:
        cleaned.sort()

    # remove order keys when sorting is complete
    value = tuple(x[1] for x in cleaned)
    # make sure set+code are entered
    value = [v for v in value if (v['set'] and v['code'])]

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
            parent = aq_parent(aq_inner(parent))
        except AttributeError:
            raise ValueError
        if IPloneSiteRoot.providedBy(parent):
            raise ValueError

    if criteria(parent): #doublecheck just to make sure
        find = parent

    if find is None:
        raise ValueError

    return find


def set_location(self, on_parent=None, object_values=None, portal_types=None):
    """ Set location helper method that sets location based on relations
        :param self: object to use as target for location field setting
        :param on_parent: boolean whether the target is self's parent
        :param object_values: ctypes to search for within self
        :param portal_types: ptypes to look for locations
    """
    first_result = False
    wftool = getToolByName(self, 'portal_workflow')
    assessment = on_parent and aq_parent(self) or self
    obj_values = object_values or 'AssessmentPart'
    p_types = portal_types or ('EEAFigure', 'DavizVisualization')

    location_json = {"type": "FeatureCollection", "features": []}
    location_json_list = location_json['features']
    locations_set = set()

    for assessment_part in assessment.objectValues(obj_values):
        for obj in assessment_part.getRelatedItems():
            if obj.portal_type in p_types:
                state = wftool.getInfoFor(obj, 'review_state', '(Unknown)')
                if state in ['published', 'visible']:
                    obj_location = obj.getLocation()
                    if not first_result:
                        if not obj_location:
                            continue
                        location_json_list.extend(
                            json.loads(obj.getField('location').getJSON(obj))
                            ['features'])
                        locations_set = set(obj_location)
                        first_result = True
                    else:
                        obj_location_set = set(obj_location)
                        if obj_location_set.issubset(locations_set):
                            continue
                        new_locations = obj_location_set.difference(
                            locations_set)
                        obj_location_json = json.loads(
                            obj.getField('location').getJSON(obj))
                        for feature in obj_location_json['features']:
                            feature_location = feature.get('properties', {})\
                                .get('description')
                            if feature_location and feature_location in \
                                    new_locations:
                                locations_set.add(feature_location)
                                location_json_list.append(feature)

    location_values = sorted(locations_set)
    location_json['features'] = sorted(location_json_list, key=lambda x:
                                x['properties']['description'])

    # set location value directly instead of using the set method defined
    # within eea.geotags field since we already have the list of locations
    field = assessment.getField('location')
    atapi.LinesField.set(field, assessment, location_values)
    translation_json = field.setTranslationJSON(assessment, location_json)
    if not translation_json:
        field.setCanonicalJSON(assessment, location_json)
