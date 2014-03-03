"""Special widgets for eea.facetednavigation
"""

from eea.facetednavigation.widgets.sorting.widget import Widget as SortingWidget
from eea.facetednavigation.interfaces import IWidgetFilterBrains
from zope.interface import implements


class IndicatorsSortingWidget(SortingWidget):
    """ Custom sorting widget for eea.facetednavigation
    """
    widget_type = 'indicators_sorting'
    widget_label = 'Indicators sorting'


class IndicatorsSorter(object):
    """A sorter for indicators"""

    implements(IWidgetFilterBrains)
    def __init__(self, context):
        self.widget = context

    def reorder_brains_codes(self):
        """Reorder brains based on codes"""

        # There is no good way of sorting a list of Specs where not all of
        #   them belong to the same indicators set, so we need to differentiate
        #   this case.
        # In this case we will sort them according to the first setcode
        #   that they present.
        codes = {}
        for brain in self.brains:
            sets = [brain.get_codes[i]
                        for i in range(0, len(brain.get_codes), 2)]
            for s in sets:
                if not s in codes:
                    codes[s] = []
                codes[s].append(brain)

        # we want to see which is the dominant setcode, which might indicate
        # a filter that was placed on the setcodes
        if not codes:
            return

        biggest = dominant = None
        for k in codes:
            if len(codes[k]) > len(codes.get(biggest, [])):
                biggest = k

        if len(codes[biggest]) == len(self.brains):
            dominant = biggest

        #dumb filtering with the first setcode
        if dominant == None:
            def get_first_setcode(b):
                """ returns """
                if b.get_codes:
                    return b.get_codes[1]
                return None
            self.brains.sort(key=get_first_setcode)
            return

        #filter the brains according to the dominant setcode
        if dominant:
            def get_dominant_setcode(b):
                """Returns """
                for i, v in enumerate(b.get_codes):
                    if v == dominant:
                        return b[i + 1]
                raise AssertionError("%s does not have the proper "
                        "value for a dominant based sorting" % b)
            self.brains.sort(key=get_dominant_setcode)
            return

    def reorder_brains_effective(self):
        """reorder"""
        self.brains.sort(key=lambda b:b.effective)
        return

    def __call__(self, brains, form):
        """ Filter brains
        """
        wid = self.widget.data.getId()
        index = form.get(wid)

        if index == "":
            return brains

        self.brains = list(brains)

        if index == "get_codes":
            self.reorder_brains_codes()

        if index == "effective":
            self.reorder_brains_effective()

        if form.get('reversed') == 'on':
            self.brains.reverse()

        return iter(self.brains)
