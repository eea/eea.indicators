# -*- coding: utf-8 -*-
#
# $Id$
#
# Copyright (c) 2010 by ['Tiberiu Ichim']
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Tiberiu Ichim <unknown>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('indicators: setuphandlers')
from eea.indicators.config import PROJECTNAME
from eea.indicators.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
##/code-section HEAD

def isNotindicatorsProfile(context):
    return context.readDataFile("indicators_marker.txt") is None

def installQIDependencies(context):
    """This is for old-style products using QuickInstaller"""
    if isNotindicatorsProfile(context): return 
    logger.info("installQIDependencies starting")
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')

    for dependency in DEPENDENCIES:
        if qi.isProductInstalled(dependency):
            logger.info("   re-Installing QI dependency %s:" % dependency)
            qi.reinstallProducts([dependency])
            transaction.savepoint() # is a savepoint really needed here?
            logger.debug("   re-Installed QI dependency %s:" % dependency)
        else:
            if qi.isProductInstallable(dependency):
                logger.info("   installing QI dependency %s:" % dependency)
                qi.installProduct(dependency)
                transaction.savepoint() # is a savepoint really needed here?
                logger.debug("   installed dependency %s:" % dependency)
            else:
                logger.info("   QI dependency %s not installable" % dependency)
                raise "   QI dependency %s not installable" % dependency
    logger.info("installQIDependencies finished")



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotindicatorsProfile(context): return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotindicatorsProfile(context): return
    site = context.getSite()

    #install dependencies available as GS profiles

    setuptool = getToolByName(site, 'portal_setup')
    importcontext = 'profile-Products.DataGridField:default_25x'
    setuptool.setImportContext(importcontext)
    setuptool.runAllImportSteps()

    logger.info("Installed dependency DataGridField")



##code-section FOOT
##/code-section FOOT
