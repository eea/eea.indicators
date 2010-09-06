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

PRODUCTS = ['DataGridField', 'ATVocabularyManager', "RedirectionTool"]

@onsetup
def setup_indicators():
    fiveconfigure.debug_mode = True

    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)
    PloneTestCase.installProduct('Five')

    try:
        import Products.FiveSite
    except ImportError:
        pass    #BBB for Plone2.5
    else:
        zcml.load_config('configure.zcml', Products.FiveSite)
        PloneTestCase.installProduct('FiveSite')

    import eea.indicators
    zcml.load_config('configure.zcml', eea.indicators)

    fiveconfigure.debug_mode = False

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
