# -*- coding: utf-8 -*-
#
# $Id$
#

""" Base classes for tests
"""

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

PRODUCTS = [
    'DataGridField', 
    'ATVocabularyManager',
    'EEAContentTypes',
    'EEAPloneAdmin',
    'UserAndGroupSelectionWidget',
    'kupu',
    #'RedirectionTool', 
]

for product in PRODUCTS:
    PloneTestCase.installProduct(product)

@onsetup
def setup_indicators():
    """Setup utilities"""
    fiveconfigure.debug_mode = True

    import eea.indicators
    zcml.load_config('configure.zcml', eea.indicators)
    PloneTestCase.installPackage('eea.indicators')

    import eea.themecentre
    zcml.load_config('configure.zcml', eea.themecentre)
    PloneTestCase.installPackage('eea.themecentre')

    import eea.relations
    zcml.load_config('configure.zcml', eea.relations)
    PloneTestCase.installPackage('eea.relations')

    import eea.workflow
    zcml.load_config('configure.zcml', eea.workflow)
    PloneTestCase.installPackage('eea.workflow')

    import eea.versions
    zcml.load_config('configure.zcml', eea.versions)
    PloneTestCase.installPackage('eea.versions')

    import eea.dataservice
    zcml.load_config('configure.zcml', eea.dataservice)
    PloneTestCase.installPackage('eea.dataservice')

    fiveconfigure.debug_mode = False

    #for product in PRODUCTS:
        #PloneTestCase.installProduct(product)

setup_indicators()
PRODUCTS.append('eea.indicators')
PloneTestCase.setupPloneSite(
        products=PRODUCTS,
        extension_profiles=
        [
            'eea.indicators:default',
            'Products.DataGridField:default',
            ]
    )


class BaseIndicatorsTestCase(PloneTestCase.FunctionalTestCase):
    """Base Test case
    """

    #def afterSetUp(self):
    #    pass

