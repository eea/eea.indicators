# -*- coding: utf-8 -*-
#
# $Id$
#
# Copyright (c) 2010 by ['Tiberiu Ichim']
#
# GNU General Public License (GPL)
#

__author__ = """Tiberiu Ichim <unknown>"""
__docformat__ = 'plaintext'

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from zope.app.component.hooks import setSite

PRODUCTS = ['DataGridField', 'ATVocabularyManager']
PROFILES = ['eea.indicators:default',]

@onsetup
def setup_indicators():
    fiveconfigure.debug_mode = True
    import Products.Five
    import Products.FiveSite
    import eea.indicators
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.FiveSite)
    zcml.load_config('configure.zcml', eea.indicators)
    fiveconfigure.debug_mode = False

    PloneTestCase.installProduct('Five')
    PloneTestCase.installProduct('FiveSite')

    for product in PRODUCTS:
        PloneTestCase.installProduct(product)


setup_indicators()
PRODUCTS.append('eea.indicators')
PloneTestCase.setupPloneSite(   
        products=PRODUCTS, 
    )


class BaseIndicatorsTestCase(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        pass
