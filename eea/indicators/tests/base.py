# -*- coding: utf-8 -*-
#
# $Id$
#

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

PRODUCTS = ['DataGridField', 'ATVocabularyManager',
            'RedirectionTool', 'FiveSite', 'ThemeCentre', ]

@onsetup
def setup_indicators():
    fiveconfigure.debug_mode = True

    fiveconfigure.debug_mode = True
    import Products.Five
    import Products.FiveSite
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.FiveSite)
    fiveconfigure.debug_mode = False

    PloneTestCase.installProduct('Five')

    #import eea.indicators
    #zcml.load_config('configure.zcml', eea.indicators)

    for product in PRODUCTS:
        PloneTestCase.installProduct(product)

setup_indicators()
PRODUCTS.append('eea.indicators')
PloneTestCase.setupPloneSite(
        products=PRODUCTS,
        #extension_profiles='eea.indicators:default'
    )


class BaseIndicatorsTestCase(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        pass
