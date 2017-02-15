""" Basic geotags storage
"""
import logging
from zope.component import queryAdapter
from eea.geotags.storage.interfaces import IGeoTags
from eea.geotags.storage.storage import GeoTags
logger = logging.getLogger('eea.indicators')

class AssessmentGeoTags(GeoTags):
    """ Geo tags storage
    """
    @property
    def tags(self):
        """ Geo tags
        """
        relatedItems = getattr(self.context,
                               'getLocationRelatedItems', lambda: [])
        geotags = {
            'type': 'FeatureCollection',
            'features': []
        }

        for ob in relatedItems():
            geo = queryAdapter(ob, IGeoTags)
            if not geo:
                continue
            features = geo.tags.get('features', [])
            geotags['features'].extend(features)
        return geotags
